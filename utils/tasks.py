#coding: utf-8
from __future__ import absolute_import
__author__ = 'moon'
from djcelery import celery
from django.core.mail import send_mail
from django.shortcuts import \
    render, \
    loader
from django.template import \
    Context

@celery.task(name = 'tasks.send_mail')
def sendmail(cont, recipient):
    send_mail(u'안녕하세요! 토마킷입니다. 정식 사용을 승인해주세요.', "",
            'makerecipe@gmail.com', recipient, fail_silently=False,
            html_message=cont)

@celery.task(name = 'tasks.send_pwchang_mail')
def send_key_email(request, title, sender, recipient,template, key, *args, **kargs):

    mail_tpl = loader.get_template(template)
    mail_ctx = Context({
        'host':request.META['HTTP_HOST'],
        'key':key,
    })
    cont = mail_tpl.render(mail_ctx)

    send_mail(title,"",sender,[recipient,],fail_silently=False, html_message=cont)

@celery.task(name = 'tasks.contact_mail')
def contact_mail(cont, recipient):
    send_mail(u'고객님이 보내신 메일입니다.', "",
            'makerecipe@gmail.com', recipient, fail_silently=False,
            html_message=cont)