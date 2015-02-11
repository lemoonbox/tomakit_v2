#coding: utf-8
__author__ = 'moon'

from django import forms
from userapp.models import Profile
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.utils.translation import ugettext as _


AlphaNumeric = RegexValidator(
    r'^[0-9a-zA-z]+$', message = _(u'영문자, 숫자만 허용됩니다.')
)

#u = UserForm(data=request.Post)

# class UserForm(forms.ModelForm):
#     password_confirm = forms.CharField(max_length=100, widget=forms.PasswordInput, validators=[AlphaNumeric,])
#     password = forms.CharField(widget=forms.PasswordInput,validators=[AlphaNumeric,])
#     class Meta:
#         model =get_user_model()
#         widgets = {
#             'password':forms.PasswordInput(),
#             'password_confirm':forms.PasswordInput(),
#         }
#         fields = ('password','password_confirm')
#
#
#
#
#     def save(self, *args, **kwargs):
#         self.username = self.email
#
#     def clean(self):
#         cleaned_data = super(UserForm, self).clean()
#
#
#
#         if cleaned_data['password'] != cleaned_data['password_confirm']:
#             self.add_error('비밀번호가 일치하지 않음.')



class ProfilesForm(forms.ModelForm):

    password_confirm = forms.CharField(max_length=100, widget=forms.PasswordInput,
                                       validators=[AlphaNumeric,], required=True)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput,
                               validators=[AlphaNumeric,], required=True)

    class Meta:
        model = Profile
        fields = ('email', 'password', 'password_confirm', 'mobile', 'address',)



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