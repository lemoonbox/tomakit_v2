__author__ = 'moon'
from django.conf.urls import url, patterns

urlpatterns = patterns('app_payment_v2d1.views',
    url(r'prefill/$', 'pay_prefill', name='pay_prefill_v2d1'),
    url(r'pay_conf/$', 'pay_conf', name="pay_conf_v2d1"),


    )