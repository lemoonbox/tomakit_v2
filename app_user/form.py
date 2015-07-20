#coding: utf-8
__author__ = 'moon'


from django import forms
from app_user.models import \
    UserProfile,\
    HostProfile
from django.contrib.auth import authenticate

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

class Host_Signup(forms.Form):

    TYPE_CHOICES = (
        (u'out', 'outclass'),
        (u'shop', 'shopclass')
    )

    mobile = forms.CharField(max_length=50, required=True)
    hosttype = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                         choices=TYPE_CHOICES)


class PwReset_RequestForm(forms.Form):

    email = forms.EmailField(max_length=100)

class Send_ConfirmForm(forms.Form):

    email = forms.EmailField(max_length=100)

class PwReset_ProcessForm(forms.Form):


    password = forms.CharField(max_length=100, widget=forms.PasswordInput, required=True)
    password_confirm = forms.CharField(max_length=100, widget=forms.PasswordInput, required=True)



class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(required=True)

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