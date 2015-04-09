__author__ = 'moon'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('app_idealine.views',



    #main page
    url(r'^$', 'idealine',name='idealine'),
    url(r'^(?P<page>[0-9]+)/$', 'idealine',name='idealine'),
    #main page class, kit, work
    #url(r'^(?P<kindof>[a-z]+)/$'),

    #catetorypage
    url(r'^category/(?P<category>[a-z]+)/$', 'categoryline', name="categoryline"),
    url(r'^category/(?P<category>[a-z]+)/(?P<page>[0-9]+)/$', 'categoryline', name="categoryline"),
    #category page class, kit, work
    #url(r'^category/(?P<category>[a-z]+)/(?P<kindof>[a-z]+)/$', 'test')

    )
