#coding: utf-8
__author__ = 'moon'
from django import forms


from app_class.models import ClassPost, ClassPic
from django.core.validators import\
    RegexValidator
from django.utils.translation import \
    ugettext as _


# Create your models here.
Numeric = RegexValidator(
    r'^[0-9]$', message = _(u'숫자만 입력해주세요')
)

Tel_Numeric = RegexValidator(
    r'^[0-9]{8,16}$', message = _(u'지역번호를 포함해서 숫자만 입력해주세요.')
)

class ClassCreateForm(forms.ModelForm):

    title_error= {'required':_(u"제목을 입력해주세요"), }
    price_error= {'required':_(u"수강료를 입력해주세요,"),
                  'invalid':_(u"숫자만 입력해주세요")}
    describe_error= {'required':_(u"강의 설명을 입해주세요."),
                     'max_length':_(u"500자 이하로 입력해주세요"),}
    lessonday_error= {'required':_(u"클래스 날짜를 입력해주세요"), }
    start_time_error= {'required':_(u"클래스 시작시간을 입력해주세요"), }
    end_time_error= {'required':_(u"클래스 종료시간을 입력해주세요"), }
    minimum_error= {'required':_(u"최소인원을 입력해주세요"),
                    'invalid':_(u"숫자만 입력해주세요")}
    maximum_error= {'required':_(u"최소인원을 입력해주세요"),
                    'invalid':_(u"숫자만 입력해주세요")}
    contact_tel_error= {'required':_(u"연락처를 입력해주세요"),
                        'invalid':_(u"숫자만 입력해주세요")}
    address_error= {'required':_(u"클래스가 열리는 주소를 입력해주세요"), }

    title = forms.CharField(error_messages=title_error)
    price = forms.IntegerField(error_messages=price_error,)
    describe = forms.CharField(max_length=500, error_messages=describe_error,)
    lessonday = forms.DateField(error_messages=lessonday_error)
    start_time = forms.TimeField(error_messages=start_time_error)
    end_time = forms.TimeField(error_messages=end_time_error)
    minimum = forms.IntegerField(error_messages=minimum_error,)
    maximum = forms.IntegerField(error_messages=maximum_error,)
    contact_tel = forms.IntegerField(error_messages=contact_tel_error)
    address = forms.CharField(error_messages=address_error)

    class Meta:
        model = ClassPost
        fields = ('title','price','describe','lessonday','start_time','end_time', 'minimum', 'maximum',
        'contact_tel', 'address')

class ClassPicCreateForm(forms.ModelForm):

    photo_error ={'required':u"한개 이상의 사진을 입력해 주세요",
                  'invalid':u'',
    }

    class_photo = forms.DateField(error_messages=photo_error)

    class Meta :
        model = ClassPic
        fields = ('class_photo',)