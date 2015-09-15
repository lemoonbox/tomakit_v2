__author__ = 'moon'
from django.conf.urls import patterns, include, url


urlpatterns = patterns('app_class_v2d1.views',
    url(r'create/begin/$', 'class_begin', name='class_create_begin_v2d1'),

    url(r"create/tut/(?P<class_num>[0-9]+)/$", 'create_tut', name="class_craete_tut_v2d1"),
    url(r"create/teach/(?P<class_num>[0-9]+)/$", 'create_teach', name="class_create_teach_v2d1"),

    url(r"modify/tut/(?P<class_num>[0-9]+)/$", 'modify_tut', name="modify_tut_v2d1"),
    url(r"modify/teach/(?P<class_num>[0-9]+)/$", "modify_teach", name="modify_teach_v2d1"),

    url(r"review/create/(?P<class_num>[0-9]+)$", 'create_review', name="create_review_v2d1"),

    )