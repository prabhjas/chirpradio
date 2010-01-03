from django.conf import settings
from django.conf.urls.defaults import *
from traffic_log.models import *
from django.views.generic import *

urlpatterns = patterns('',
    url(r'^/?$', 'traffic_log.views.index', name='trafficlog.index'),
    (r'^spot/?$','traffic_log.views.listSpots'),
    (r'^spot/create/?$', 'traffic_log.views.createSpot'),
    (r'^spot/text-for-reading/(?P<spot_key>[^\./]+)$', 'traffic_log.views.spotTextForReading'),
    (r'^spot/edit/(?P<spot_key>[^\.^/]+)$', 'traffic_log.views.editSpot'),
    (r'^spot/delete/(?P<spot_key>[^\.^/]+)$', 'traffic_log.views.deleteSpot'),
    (r'^spot/(?P<spot_key>[^\.^/]+)/?$', 'traffic_log.views.spotDetail'),                       
    (r'^spot_constraint/delete/(?P<spot_constraint_key>[^\.^/]+)/spot/(?P<spot_key>[^\.^/]+)?$',
     'traffic_log.views.deleteSpotConstraint'),
    # kumar: commenting this out for now since the view function doesn't exist 
    # (r'^generate/(\d{4})/(\d{2})/(\d{2})','traffic_log.views.generateTrafficLog')
    )

