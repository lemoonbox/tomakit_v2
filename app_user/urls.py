__author__ = 'moon'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('app_user.views',
    #signnup
    url(r'signup/$', 'signup', name='v2_signup'),
    url(r'signup/confirm/(?P<key>[\w.@+-]+)/$', 'signup_confirm', name="v2_email_confirm"),
    url(r'send_confirm/$', 'send_confirm', name='v2_send_confirm'),
    url(r'signup/host/$', 'host_signup', name='v2_host_signup'),


    url(r'reset_password/$', 'pw_reset_request', name="v2_reset_request"),
    url(r'reset_process/(?P<key>[\w.@+-]+)/$', 'pw_reset_process', name='pw_reset_process_get'),
    url(r'reset_process/$', 'pw_reset_process', name='pw_reset_process_get')
)
