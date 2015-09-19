__author__ = 'moon'
from django.conf.urls import patterns, include, url


urlpatterns = patterns('app_class_v2d1.views',

    #create
    url(r'create/begin/$', 'class_begin', name='class_create_begin_v2d1'),
    url(r"create/tut/(?P<class_num>[0-9]+)/$", 'create_tut', name="class_craete_tut_v2d1"),
    url(r"create/teach/(?P<class_num>[0-9]+)/$", 'create_teach', name="class_create_teach_v2d1"),

    #modify
    url(r"modify/tut/(?P<class_num>[0-9]+)/$", 'modify_tut', name="modify_tut_v2d1"),
    url(r"modify/teach/(?P<class_num>[0-9]+)/$", "modify_teach", name="modify_teach_v2d1"),

    #onoff
    url(r"onoff/(?P<class_type>[a-z,_]+)/(?P<card_num>[0-9]+)", 'class_onoff', name="onoff_class_v2d1"),

    #detail
    url(r'(?P<class_num>[0-9]+)/$', 'class_post_detail', name='class_detail_v2d1'),

    url(r"review/create/(?P<class_num>[0-9]+)$", 'create_review', name="create_review_v2d1"),
    url(r"review/modify/(?P<class_num>[0-9]+)$", 'modify_review', name="modify_review_v2d1"),
    url(r"review/delete/(?P<review_num>[0-9]+)$", 'delete_review', name="delete_review_v2d1"),

    )