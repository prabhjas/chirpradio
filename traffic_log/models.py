###
### Copyright 2009 The Chicago Independent Radio Project
### All Rights Reserved.
###
### Licensed under the Apache License, Version 2.0 (the "License");
### you may not use this file except in compliance with the License.
### You may obtain a copy of the License at
###
###     http://www.apache.org/licenses/LICENSE-2.0
###
### Unless required by applicable law or agreed to in writing, software
### distributed under the License is distributed on an "AS IS" BASIS,
### WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
### See the License for the specific language governing permissions and
### limitations under the License.
###

import random
import datetime

from google.appengine.ext import db, search
from django.core.urlresolvers import reverse

from auth.models import User
from traffic_log import constants
from common.autoretry import AutoRetry
from common import time_util

class SpotAtConstraint(object):
    """A spot within its constraint."""
    
    def __init__(self, spot_constraint, spot):
        self.spot = spot
        
        q = (TrafficLogEntry.all()
                .filter("log_date =", time_util.chicago_now().date())
                .filter("spot =", spot)
                .filter("hour =", spot_constraint.hour)
                .filter("slot =", spot_constraint.slot)
                .filter("dow =", spot_constraint.dow))
        if AutoRetry(q).count(1):
            self.finished = True
        else:
            self.finished = False

class SpotConstraint(db.Model):
    dow      = db.IntegerProperty(verbose_name="Day of Week", choices=constants.DOW)
    hour     = db.IntegerProperty(verbose_name="Hour", choices=constants.HOUR)
    slot     = db.IntegerProperty(verbose_name="Spot", choices=constants.SLOT)
    spots    = db.ListProperty(db.Key)
    
    def iter_spots(self):
        for spot in AutoRetry(Spot).get(self.spots):
            yield spot
    
    def iter_spots_at_constraint(self):
        for spot in self.iter_spots():
            yield SpotAtConstraint(self, spot)
    
    def as_query_string(self):
        return "hour=%d&dow=%d&slot=%d" % (self.hour, self.dow, self.slot)
    
    def url_to_finish_spot(self, spot):
        url = ""
        if len(spot.random_spot_copies) > 0:
            url = reverse('traffic_log.finishReadingSpotCopy', args=(spot.random_spot_copies[0],))
            url = "%s?%s" % (url, self.as_query_string())
        return url
    
    @property
    def readable_slot_time(self):
        min_slot = str(self.slot)
        if min_slot == '0':
            min_slot = '00'
        meridian = 'am'
        hour = self.hour
        if hour > 12:
            meridian = 'pm'
            hour = hour - 12
        # exceptions:
        if hour == 12:
            meridian = 'pm'
        if hour == 0:
            hour = 12
        return "%s:%s%s" % (hour, min_slot, meridian)

    def __init__(self, *args, **kw):
        key_name = "%d:%d:%d" % (kw['dow'], kw['hour'], kw['slot']) 
        super(SpotConstraint, self).__init__(*args, **kw)


class Spot(db.Model):
    """
    """
    title     = db.StringProperty(verbose_name="Spot Title", required=True)
    type      = db.StringProperty(verbose_name="Spot Type", required=True, choices=constants.SPOT_TYPE)
    created   = db.DateTimeProperty(auto_now_add=True)
    updated   = db.DateTimeProperty(auto_now=True)
    random_spot_copies = db.ListProperty(db.Key)

    def all_spot_copy(self):
        # two queries (since there is no OR statement).  
        # One for copy that does not expire and one for not-yet-expired copy
        q = SpotCopy.all().filter("spot =", self).filter("expire_on =", None)
        active_spots = [c for c in AutoRetry(q)]
        q = SpotCopy.all().filter("spot =", self).filter("expire_on >", datetime.datetime.now())
        for c in AutoRetry(q):
            active_spots.append(c)
        return active_spots

    def add_spot_copy(self, spot_copy):
        self.random_spot_copies.append(spot_copy.key())
        AutoRetry(self).save()

    def shuffle_spot_copies(self, prev_spot_copy=None):
        # Shuffle list of spot copy keys associated with this spot.
        spot_copies = [spot_copy.key() for spot_copy in self.all_spot_copy()]
        random.shuffle(spot_copies)

        # Get spot copies that have been read in the last period (two hours).
        date = datetime.datetime.now().date() - datetime.timedelta(hours=2)
        query = TrafficLogEntry.all().filter('log_date >=', date)
        recent_spot_copies = []
        for entry in query:
            recent_spot_copies.append(entry.spot_copy.key())
		
        # Iterate through list, moving spot copies that have been read in the past period to the
        # end of the list.
        for i in range(len(spot_copies)):
            if spot_copies[0] in recent_spot_copies:
                spot_copies.append(spot_copies.pop(0))
		
        # If all spot copies were read in the last period, the first item in the new shuffled list
        # may by chance be the last one read. If so, move to the end.
        if prev_spot_copy and spot_copies[0] == prev_spot_copy:
            spot_copies.append(spot_copies.pop(0))
            
        self.random_spot_copies = spot_copies

    def get_spot_copy(self, dow, hour, slot):
        spot_copy = None
        is_logged = False

        # If random spot copy list for this spot is empty, fill and shuffle.
        if len(self.random_spot_copies) == 0:
            self.shuffle_spot_copies()
            AutoRetry(self).save()
        
        # Return previous spot copy, or next random one.
        if len(self.random_spot_copies) > 0:
            today = time_util.chicago_now().date()
            q = (TrafficLogEntry.all()
                    .filter("log_date =", today)
                    .filter("spot =", self)
                    .filter("dow =", dow)
                    .filter("hour =", hour)
                    .filter("slot =", slot))
                    
            # Spot copy exists for dow, hour, and slot. Return it.
            if AutoRetry(q).count(1):
                existing_logged_spot = AutoRetry(q).fetch(1)[0]
                spot_copy = existing_logged_spot.spot_copy
                is_logged = True
                
            # Return next random spot copy.
            else:
                spot_copy = AutoRetry(db).get(self.random_spot_copies[0])
                
        return spot_copy, is_logged

    def finish_spot_copy(self):
        # Pop off spot copy from this spot's shuffled list of spot copies.
        spot_copy = self.random_spot_copies.pop(0)
        
        # If shuffled spot copy list is empty, regenerate.
        if len(self.random_spot_copies) == 0:
            self.shuffle_spot_copies(spot_copy)
            
        AutoRetry(self).save()

    @property
    def constraints(self):
        return SpotConstraint.gql("where spots =:1 order by dow, hour, slot", self.key())

    def get_add_copy_url(self):
        return reverse('traffic_log.views.addCopyForSpot', args=(self.key(),))

    def get_absolute_url(self):
        return '/traffic_log/spot/%s/' % self.key()

class SpotCopy(db.Model):
    
    spot        = db.ReferenceProperty(Spot)
    underwriter = db.TextProperty(required=False)
    body        = db.TextProperty(verbose_name="Spot Copy",  required=True)
    expire_on   = db.DateTimeProperty(verbose_name="Expire Date", required=False, default=None)
    author      = db.ReferenceProperty(User)
    created     = db.DateTimeProperty(auto_now_add=True)
    updated     = db.DateTimeProperty(auto_now=True)
    
    def __unicode__(self):
        body_words = self.body.split(" ")
        def shorten(words, maxlen=55):
            s = ' '.join(words)
            if len(s) > maxlen:
                words.pop()
                return shorten(words)
            else:
                return s
        shortened_body = shorten([w for w in body_words])
        return u"%s..." % shortened_body
    
    __str__ = __unicode__

    def get_absolute_url(self):
        return '/traffic_log/spot-copy/%s/' % self.key()

    def get_delete_url(self):
        return reverse('traffic_log.deleteSpotCopy', args=(self.key(),))

    def get_edit_url(self):
        return reverse('traffic_log.editSpotCopy', args=(self.key(),))

## there can only be one entry per date, hour, slot
class TrafficLogEntry(db.Model):
    log_date  = db.DateProperty()
    spot      = db.ReferenceProperty(Spot)
    spot_copy = db.ReferenceProperty(SpotCopy)
    dow       = db.IntegerProperty()
    hour      = db.IntegerProperty()
    slot      = db.IntegerProperty()
    scheduled = db.ReferenceProperty(SpotConstraint)
    readtime  = db.DateTimeProperty()
    reader    = db.ReferenceProperty(User)
    created   = db.DateTimeProperty(auto_now_add=True)

    
