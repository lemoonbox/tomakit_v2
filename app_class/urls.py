__author__ = 'moon'
from django.conf.urls import patterns, include, url
import django_summernote.urls

urlpatterns = patterns('app_class.views',


    url(r'^create/', 'classcreate',name='classcreate'),
    url(r'^summernote/', include('django_summernote.urls')),

    #url(r'^(?P<class_num>[0-9]+)/$', 'class_detail', name="class_detail"),
    )
