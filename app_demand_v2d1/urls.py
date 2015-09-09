__author__ = 'moon'
from django.conf.urls import patterns, include, url


urlpatterns = patterns('app_demand_v2d1.views',
    url(r'create/$', 'demand_create', name='demand_create_v2d1'),
    )