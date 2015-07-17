#coding: utf-8
__author__ = 'moon'


from django import forms
from app_user.models import UserProfile
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):

    username_errors={'required':u"이메일이 필요합니다.",
                    'invalid':u'잘못된 이메일 형식입니다.',
                    'unique':u'이미 사용 중인 이메일 주소입니다.'}
    pw_errors={'required':u"비밀번호가 필요합니다."}

    username = forms.EmailField(error_messages=username_errors,)


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','password')