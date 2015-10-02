__author__ = 'moon'
__author__ = 'moon'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('app_board_v2d1.views',

    #question board
    url("mainpage/$", "mainpage", name="mainpage_v2d1"),

    url("class_list/$", 'class_list_board', name='class_list_v2d1'),
    url("class_list/(?P<page>[0-9]+)/$", 'class_list_board', name="class_list_paging_v2d1"),
    url("class_list/(?P<page>[0-9]+)/(?P<category>[a-z,_,0-9]+)/(?P<state>[a-z,_,0-9]+)/$",
        'class_list_board', name="class_list_paging_v2d1"),

    url("class_filter/$", 'class_filter_redirect', name="class_filter_redirct_v2d1"),

    url("demand_list/$", 'demand_list_board', name='demand_list_v2d1'),
    url("demand_list/(?P<page>[0-9]+)/$", 'demand_list_board', name="demand_list_paging_v2d1"),
    url("demand_list/(?P<page>[0-9]+)/(?P<category>[a-z,_,0-9]+)/(?P<state>[a-z,_,0-9]+)/$",
        'demand_list_board', name="demand_class_list_paging_v2d1"),

    url("demand_filter/$", "demand_filter_redirect", name="demnad_filter_redirct_v2d1")


    )