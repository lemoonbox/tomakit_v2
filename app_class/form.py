#coding: utf-8
__author__ = 'moon'
from django import \
    forms
from django.core.validators import\
    RegexValidator
from django.utils.translation import \
    ugettext as _


from app_class.models import ClassPost, PriceTag, ClassPic, Review

class ClassForm(forms.ModelForm):

    title_error= {'required':_(u"제목을 입력해주세요"), }
    price_error= {'required':_(u"수강료를 입력해주세요"),
                  'invalid':_(u"숫자만 입력해주세요")}
    day_error= {'required':_(u"수업날자를 입력해주세요"), }
    time_error= {'required':_(u"수업날자를 입력해주세요"), }
    mem_num_error= {'required':_(u"몇명까지 모집하시는지 입력해주세요"),
                    'invalid':_(u"숫자만 입력해주세요")}
    contact_tel_error= {'required':_(u"연락처를 입력해주세요"),
                        'invalid':_(u"숫자만 입력해주세요")}
    address_error= {'required':_(u"클래스가 열리는 주소를 입력해주세요"), }
    video_url_error= {'invalid':_(u"정상적인 메일 주소를 입력해주세요"),}
    need_error={'required':_(u"어떤 사람에게 좋은 수업인가요?"), }


    title = forms.CharField(error_messages=title_error)
    price = forms.IntegerField(error_messages=price_error,)
    day=forms.CharField(error_messages=day_error)
    time=forms.CharField(error_messages=time_error)
    mem_num=forms.IntegerField(error_messages=mem_num_error,)
    contact_tel = forms.IntegerField(error_messages=contact_tel_error)
    address = forms.CharField(error_messages=address_error)
    video_url=forms.URLField(required=False, error_messages=video_url_error)
    need1=forms.CharField(error_messages=need_error)
    need2=forms.CharField(error_messages=need_error)
    need1_detail=forms.CharField(error_messages=need_error)
    need2_detail=forms.CharField(error_messages=need_error)

    class Meta:
        model = ClassPost
        fields = ('title','price', 'day', 'time', 'mem_num', 'contact_tel', 'address'
        ,'video_url', 'need1', 'need1_detail', 'need2', 'need2_detail')

class Price_Tag_Form(forms.ModelForm):

    price_tag_error ={'required':u"한개 이상의 태그를 입력해주세요",
                  'invalid':u'',
    }

    price_tag = forms.CharField(error_messages=price_tag_error)

    class Meta :
        model = PriceTag
        fields = ('price_tag',)

class ClassPicForm(forms.ModelForm):

    class_photo_error ={'invalid':u'',}

    class_photo = forms.ImageField(required=False, error_messages=class_photo_error)

    class Meta :
        model = ClassPic
        fields = ('class_photo',)

class ReviewForm(forms.ModelForm):

    review_error={'required':u"내용을 입력 해주세요.",}
    reviewer_name_error={'required':u"리뷰어 이름을 입력해주세요.",}
    reviewer_photo_error ={'required':u"사진을 지정해주세요.",
        'invalid':u'',}

    review=forms.CharField(error_messages=review_error)
    reviewer_name=forms.CharField(error_messages=reviewer_name_error)
    reviewer_photo = forms.ImageField(error_messages=reviewer_photo_error)

    class Meta :
        model = Review
        fields = ('review', 'reviewer_photo', 'reviewer_name')

class ClassCurriForm(forms.ModelForm):

    curri_name_error={'required':u"단계 이름을 입력해 주세요.",}
    curri_detail_error={'required':u"상세 설명을 입력해주세요.",}

    curri_name=forms.CharField(error_messages=curri_name_error)
    curri_detail=forms.CharField(error_messages=curri_detail_error)

    class Meta :
        model = Review
        fields = ('curri_name', 'curri_detail')