__author__ = 'moon'
from django.conf.urls import patterns, include, url


urlpatterns = patterns('app_demand_v2d1.views',
    url(r'create/$', 'demand_create', name='demand_create_v2d1'),
    url(r'modify/(?P<demand_num>[0-9]+)/$', 'demand_modify', name='demand_modify_v2d1')
    )