from __future__ import absolute_import
#coding: utf-8
__author__ = 'moon'
from djcelery import celery
from django.core.mail import send_mail

@celery.task(name = 'tasks.send_mail')
def sendmail(cont, recipient):
    send_mail(u'안녕하세요! 앞발 사용 설명서입니다. 정식 사용을 승인해주세요.', "",
            'makerecipe@gmail.com', recipient, fail_silently=False,
            html_message=cont)

@celery.task(name = 'tasks.send_pwchang_mail')
def send_pwchang_mail(cont, recipient):
    send_mail(u'다음 링크를 클릭하면 패스워드를 바꾸실 수 있습니다.', "",
            'makerecipe@gmail.com', recipient, fail_silently=False,
            html_message=cont)

@celery.task(name = 'tasks.contact_mail')
def contact_mail(cont, recipient):
    send_mail(u'고객님이 보내신 메일입니다.', "",
            'makerecipe@gmail.com', recipient, fail_silently=False,
            html_message=cont)


# @celery.task(name = 'tasks.rabbitmqtest')
# def rabbitmqtest():
#     print "task test"
#
# from celery import shared_task
# @shared_task
# def add(x, y):
#     return x + y
#
# @shared_task
# def mul(x, y):
#     return x * y
#
# @shared_task
# def xsum(numbers):
#     return sum(numbers)