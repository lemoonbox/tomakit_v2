__author__ = 'moon'
from django.conf.urls import patterns, url


urlpatterns = patterns('app_kit.views',

        url(r'^create/', 'kitcreate', name='kitcreate'),
        url(r'^(?P<kit_num>[0-9]+)/$', 'kit_detail', name="class_detail"),

)