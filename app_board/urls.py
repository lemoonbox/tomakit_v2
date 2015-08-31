__author__ = 'moon'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('app_board.views',

    #question board
    url(r'^questionboard/$', 'questionboard',name='v2_questionboard'),
    url(r'^questionboard/(?P<page>[0-9]+)/$', 'questionboard', name='v2_questionboard_paging'),
    url(r'^questionboard/(?P<page>[0-9]+)/(?P<category>[a-z,_]+)/(?P<state>[a-z,_]+)/$', 'questionboard', name='v2_questionboard_paging'),

    url(r'^caseboard/$', 'caseboard',name='v2_questionboard'),
    url(r'^caseboard/(?P<page>[0-9]+)/$', 'caseboard', name='v2_questionboard_paging'),
    url(r'^caseboard/(?P<page>[0-9]+)/(?P<category>[a-z,_]+)/(?P<state>[a-z,_]+)/$', 'caseboard', name='v2_questionboard_paging'),

    )
