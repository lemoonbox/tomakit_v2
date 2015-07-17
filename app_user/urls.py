__author__ = 'moon'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('app_user.views',
    #signnup
    url(r'signup/$', 'signup', name='v2_signup'),

)
