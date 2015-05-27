__author__ = 'moon'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('userapp.views',


    url(r'profile/', 'profile',name='profile'),

    url(r'login/', 'login', {'template_name':'userapp/login.html'}, name="login_url"),
    url(r'^logout/$', 'logout', {'next_page':'/'}, name = "logout_url"),


    #signnup
    url(r'signup/$', 'signup', name='signup'),
    url(r'signup_confirm/(?P<key>[\w.@+-]+)/$', 'signup_confirm', name="email_confirm"),
    url(r'userprivacy/$', 'userprivacy', name="userprivacy"),

    #sellersignup
    url(r'signup/seller', 'sellersignup', name='sellersignup'),

    #chang pw
    url(r'reset_password/$', 'pw_reset_request', name='pw_reset_request'),
    url(r'reset_process/(?P<key>[\w.@+-]+)/$', 'pw_reset_process', name='pw_reset_process_get'),
    url(r'reset_process/$', 'pw_reset_process', name='pw_reset_process_post'),

    #contact
    url(r'contact/$', 'contactemail', name='sendemail'),
)
