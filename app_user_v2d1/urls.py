__author__ = 'moon'
from django.conf.urls import patterns, include, url


urlpatterns = patterns('app_user_v2d1.views',
    url(r'signup/$', 'signup', name='signup_v2d1'),
    url(r'signup/confirm/(?P<key>[\w.@+-]+)/$', 'signup_confirm', name="email_confirm_v2d1"),
    url(r'send_conf/$', 'send_confirm', name="send_conf_v2d1"),

    url(r'pw_reset/$', 'pw_reset_request', name='reset_pw_req'),
    url(r'reset_process/(?P<key>[\w.@+-]+)/$', 'pw_reset_process', name='reset_process_v2d1'),
    url(r'reset_process/$', 'pw_reset_process', name='reset_process_v2d1'),

    url(r'login/$', 'login', name='login_v2d1'),
    )