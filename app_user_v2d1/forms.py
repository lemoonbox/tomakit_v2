#coding: utf-8
__author__ = 'moon'
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from app_user_v2d1.models import \
    T2HostApply


class UserForm(forms.ModelForm):

    username_errors={'required':u"이메일이 필요합니다.",
                    'invalid':u'잘못된 이메일 형식입니다.',
                    'unique':u'이미 사용 중인 이메일 주소입니다.'}
    pw_errors={'required':u"비밀번호가 필요합니다."}

    username = forms.EmailField(error_messages=username_errors,)


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','password')


class LoginForm(forms.Form):
    username=forms.CharField(max_length=255, required=True)
    password=forms.CharField(max_length=100, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username = username, password=password)
        if not user or not user.is_active:
            self.add_error('username', '아이디 혹은 비밀번호가 잘못되었습니다.')
        return self.cleaned_data

    def authenticate(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user.has_usable_password():
            return user
        else :
            return None

class EmailCheck(forms.ModelForm):

    username_errors={'required':u"이메일이 필요합니다.",
                    'invalid':u'잘못된 이메일 형식입니다.',
                    'unique':u'입력하신 주소로 변경 이메일이 발송 되었습니다.'}

    username = forms.EmailField(max_length=100, error_messages=username_errors)

    class Meta:
        model = User
        fields = ('username',)

class PW_CrossCheckForm(forms.Form):


    password = forms.CharField(max_length=100, widget=forms.PasswordInput, required=True)
    password_confirm = forms.CharField(max_length=100, widget=forms.PasswordInput, required=True)

    def is_valid(self):

        valid = super(PW_CrossCheckForm, self).is_valid()

        if not valid:
            return valid

        if (self.cleaned_data['password']!=
                self.cleaned_data['password_confirm']):
            return False

        return True

class HostApplyForm(forms.ModelForm):

    required_error={'required':u"필수 항목 입니다."}
    num_error={"invalid":u"숫자만 입력해주세요"}
    url_error={"invlaid":u"url주소를 입력해주세요."}
    mobli_error={}
    mobli_error.update(required_error)
    mobli_error.update(num_error)
    site_error={}
    site_error.update(required_error)
    site_error.update(url_error)

    introduce=forms.CharField(max_length=100, error_messages=required_error)
    mobli1=forms.IntegerField(error_messages=mobli_error)
    mobli2=forms.IntegerField(error_messages=mobli_error)
    mobli3=forms.IntegerField(error_messages=mobli_error)
    hosttype=forms.CharField(error_messages=required_error)
    local=forms.CharField(error_messages=required_error)
    site=forms.URLField(error_messages=site_error)
    potpolio=forms.FileField(required=False)

    class Meta:
        model=T2HostApply
        fields = ('introduce', 'mobli', 'hosttype', 'local', 'site', "potpolio")