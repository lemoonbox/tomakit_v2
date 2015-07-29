#coding: utf-8
__author__ = 'moon'


from django import forms

from app_question.models import QItem, QSkill


class CreateQItem(forms.ModelForm):

    title_error ={'required':u"배우고 싶은 것을 입력해 주세요",}
    mylocal_error ={'required':u"수업 지역을 입력해주세요",}
    wantedu_error ={'required':u"무엇을 배우고 싶으신지 입력해주세요",}
    memnum_error={'required':u"수강인원은 몇명인가요?",}
    mobile_error={'required':u"전화번호를 입력해주세요.",}


    title = forms.CharField(required=True, error_messages=title_error)
    mylocal = forms.CharField(required=True, error_messages=mylocal_error)
    wantedu = forms.CharField(required=True, widget=forms.Textarea, error_messages=wantedu_error)
    memnum = forms.IntegerField(required=True, error_messages=memnum_error)
    mobile = forms.CharField(required=True, error_messages=mobile_error)
    qpic = forms.ImageField(required=False)

    class Meta:
        model = QItem
        exclude = ('djgouser','category', 'state')
        field = ('title', 'mylocal', 'wantedu', 'memnum', 'mobile')



class CreateQSkill(forms.ModelForm):



    title_error ={'required':u"배우고 싶은 것을 입력해 주세요",}
    mylocal_error ={'required':u"수업 지역을 입력해주세요",}
    class_error ={'required':u"찾고 있는 수업의 특징을 입력해주세요",}
    goal_error ={'required':u"원하시는 목표를 입력해주세요",}
    wantedu_error ={'required':u"무엇을 배우고 싶으신지 입력해주세요",}
    memnum_error={'required':u"수강인원은 몇명인가요?",}
    mobile_error={'required':u"전화번호를 입력해주세요.",}


    title = forms.CharField(required=True, error_messages=title_error)
    mylocal = forms.CharField(required=True, error_messages=mylocal_error)
    wantclass = forms.CharField(required=False, widget=forms.Textarea, error_messages=class_error)
    wantgoal = forms.CharField(required=False, widget=forms.Textarea, error_messages=goal_error)
    wantedu = forms.CharField(required=False, widget=forms.Textarea, error_messages=wantedu_error)
    memnum = forms.IntegerField(required=True, error_messages=memnum_error)
    mobile = forms.CharField(required=True, error_messages=mobile_error)

    class Meta:
        model = QSkill
        exclude = ('djgouser','category', 'state')
        field = ('title', 'mylocal', 'wanclass', 'wantgoal', 'wantedu', 'memnum', 'mobile')