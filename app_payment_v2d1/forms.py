#coding: utf-8
__author__ = 'moon'

from django import forms




class PayPrefillForm(forms.Form):

    required_error={'required':u"필수 항목입니다."}
    num_error={'invalid':u"숫자만 입력해주세요"}
    mobli_error={}
    mobli_error.update(required_error)
    mobli_error.update(num_error)

    buyer_name=forms.CharField(error_messages=required_error)
    buyer_email=forms.CharField(error_messages=required_error)
    mobli1=forms.IntegerField(error_messages=mobli_error)
    mobli2=forms.IntegerField(error_messages=mobli_error)
    mobli3=forms.IntegerField(error_messages=mobli_error)
    want_day=forms.DateField(required=False)
    pay_method=forms.CharField(error_messages=required_error)