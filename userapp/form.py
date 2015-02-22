#coding: utf-8
__author__ = 'moon'

from django import forms
from userapp.models import Profile
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.utils.translation import ugettext as _


AlphaNumeric = RegexValidator(
    r'^[0-9a-zA-z@.]{1,}$', message = _(u'알파벳과, 숫자만 허용됩니다.')
)

class ProfilesForm(forms.ModelForm):

    email_errors={'required':u"이메일이 필요합니다.",
                    'invalid':u'잘못된 이메일 형식입니다.',
                    'unique':u'이미 사용중 이메일 주소입니다.'}
    pw_errors={'required':u"비밀번호가 필요합니다.",
                'invalid':u"6자리 이상의 비밀번호가 안전합니다."}
    image_errors={'invalid_image':u"이미지 파일만 올릴 수 있습니다."}
    email = forms.EmailField(error_messages=email_errors,
                            validators=[AlphaNumeric,])
    password = forms.CharField(max_length=100, widget=forms.PasswordInput,
                           validators=[AlphaNumeric,], required=True,
                           error_messages=pw_errors, label=u'비밀번호')
    password_confirm = forms.CharField(max_length=100, widget=forms.PasswordInput,
                                       validators=[AlphaNumeric,], required=True,
                                       error_messages=pw_errors, label=u'비밀번호확인')
    pro_photo = forms.ImageField(required=False, label=u'프로필이미지(선택)',
                                 error_messages = image_errors)

    class Meta:
        model = Profile
        fields = ('email', 'password', 'password_confirm','pro_photo')



class PwReset_RequestForm(forms.Form):

    email = forms.EmailField(max_length=100)




class PwReset_ProcessForm(forms.Form):


    password = forms.CharField(max_length=100, widget=forms.PasswordInput,
                               validators=[AlphaNumeric,], required=True)
    password_confirm = forms.CharField(max_length=100, widget=forms.PasswordInput,
                                       validators=[AlphaNumeric,], required=True)

    class Meta:
        model = Profile
        fields = ('password', 'password_confirm',)