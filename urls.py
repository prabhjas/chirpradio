# Copyright 2008 Google Inc.
# Copyright 2009 The Chicago Independent Radio Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns(
    '',
    # To ensure that each the URL-spaces exposed by applications are
    # unique, URLs should be prefixed with a path component identical
    # to the application's name.  For example: if the volunteer
    # tracker app lives under the 'volunteers' subdirectory, each of
    # that app's URLs should be of the form
    # http://host/volunteers/XXXXX.

    # The lone exception to our URL naming convention is the main
    # landing page.
    ('^$', 'landing_page.views.landing_page'),

    # A hack to serve the favicon, which we store in common.
    (r'^favicon.ico$', 'django.views.static.serve',
     {'document_root': 'common', 'path': 'favicon.ico',
      }),

    # The site authentication system.
    ('^auth/', include('auth.urls')),

    # The DJ database.
    ('^djdb/', include('djdb.urls')),
    
    # DJ Playlists.
    ('^playlists/', include('playlists.urls')),

    # The volunteer management app.
    ('^volunteers/', include('volunteers.urls')),

    (r'^traffic_log/?', include('traffic_log.urls')),   
)
