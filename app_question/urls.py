__author__ = 'moon'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('app_question.views',


    url(r'^item/create/', 'create_q_item',name='v2_create_q_item'),
    url(r'^item/(?P<qitem_num>[0-9]+)/$', 'qitem_detail', name="v2_qitem_detail"),

    )
