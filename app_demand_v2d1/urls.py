__author__ = 'moon'
from django.conf.urls import patterns, include, url


urlpatterns = patterns('app_demand_v2d1.views',
    url(r'create/$', 'demand_create', name='demand_create_v2d1'),
    url(r'modify/(?P<demand_num>[0-9]+)/$', 'demand_modify', name='demand_modify_v2d1'),

    url(r"mobli/(?P<post_num>[0-9]+)/", 'mobli_required', name='mobli_require_v2d1'),



    url(r"comment/create/(?P<demand_num>[0-9]+)$", 'create_comment', name="create_comment_v2d1"),
    url(r"comment/modify/(?P<demand_num>[0-9]+)$", 'modify_comment', name="modify_comment_v2d1"),
    url(r"comment/delete/(?P<comment_num>[0-9]+)$", 'delete_comment', name="delete_comment_v2d1"),


    url(r"lineup/(?P<demand_num>[0-9]+)/$", 'lineup_demand', name='lineup_demand_v2d1'),
    url(r"lineup/(?P<demand_num>[0-9]+)/(?P<page>[0-9]+)/(?P<category>[a-z,_]+)/(?P<state>[a-z,_]+)/$",
        'lineup_demand', name="lineup_pageing_v2d1"),

    url(r'(?P<demand_num>[0-9]+)/$', 'demand_detail', name="demand_detial_v2d1"),
    )