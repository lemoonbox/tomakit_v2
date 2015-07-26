__author__ = 'moon'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('app_question.views',


    url(r'^item/create/', 'create_q_item',name='classcreate'),

    )
