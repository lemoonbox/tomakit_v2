#coding: utf-8
__author__ = 'moon'
from django import \
    forms
from django.core.validators import\
    RegexValidator
from django.utils.translation import \
    ugettext as _
from django.forms.widgets import Select


from django_summernote.widgets import \
    SummernoteWidget, \
    SummernoteInplaceWidget
from django_summernote import \
    fields as summer_fields

from app_class.models import ClassPost, ClassPic, ClassDetail

# Create your models here.
Numeric = RegexValidator(
    r'^[0-9]$', message = _(u'숫자만 입력해주세요')
)

Tel_Numeric = RegexValidator(
    r'^[0-9]{8,16}$', message = _(u'지역번호를 포함해서 숫자만 입력해주세요.')
)

CATEGORY_SELECT =((1,'for Baby'),
                  (2,'for Home'),
                  (3, 'for Funny'),
                  (4, 'for Art'),
                  (5, 'for Fashion'),
                  (6,'for Tast'),
                  (7, 'for Beauty'),)

class ClassCreateForm(forms.ModelForm):

    category_error= {'required':_(u"카테고리를 입력해주세요"), }
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


    category = forms.MultipleChoiceField(required=True,
                                         widget=forms.CheckboxSelectMultiple,
                                         choices=CATEGORY_SELECT,
                                         error_messages=category_error)
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
        fields = ('category', 'title','price','describe','lessonday','start_time','end_time', 'minimum', 'maximum',
        'contact_tel', 'address')


class ClassPicCreateForm(forms.ModelForm):

    photo_error ={'required':u"한개 이상의 사진을 입력해 주세요",
                  'invalid':u'',
    }

    class_photo = forms.DateField(error_messages=photo_error)

    class Meta :
        model = ClassPic
        fields = ('class_photo',)



class ClassdetailForm(forms.ModelForm):

    class_detail_error= {'required':_(u"상세한 정보를 입력해주세요"), }

    class_detail = summer_fields.SummernoteTextFormField(error_messages=class_detail_error,
                                                         label='')
    class Meta:
        model = ClassDetail
        fields = ('class_detail',)
        widgets = {
            'foo': SummernoteWidget(),
            'bar': SummernoteInplaceWidget(),
        }
