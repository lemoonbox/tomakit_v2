__author__ = 'moon'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('app_post.views',


    url(r'^class/create/', 'classcreate',name='classcreate'),
    url(r'^kit/create/', 'kitcreate',name='kitcreate'),

    url(r'^class/(?P<class_num>[0-9]+)/$', 'class_detail', name="class_detail"),
    url(r'^kit/(?P<kit_num>[0-9]+)/$', 'kit_detail', name="kit_detail"),
    )
