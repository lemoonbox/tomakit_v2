__author__ = 'moon'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('app_class.views',


    url(r'^create/', 'classcreate',name='classcreate'),

    url(r'^(?P<class_num>[0-9]+)/$', 'class_detail', name="class_detail"),
    )
