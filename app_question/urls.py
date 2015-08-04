__author__ = 'moon'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('app_question.views',

    #item
    url(r'^item/create/', 'create_q_item',name='v2_create_q_item'),
    url(r'^item/(?P<qitem_num>[0-9]+)/$', 'qitem_detail', name="v2_qitem_detail"),

    url(r'^skill/create/', 'create_q_skill',name='v2_create_q_skill'),
    url(r'^skill/(?P<qskill_num>[0-9]+)/$', 'qskill_detail', name="v2_qskill_detail"),

    url(r'^next_guid/$', 'next_guid', name='v2_next_guid'),


    )
