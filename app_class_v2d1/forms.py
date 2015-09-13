#coding: utf-8
__author__ = 'moon'
from django import forms

from app_class_v2d1.models import \
    T2TutClass, \
    T2TeachClass



class T2Class_BeginForm(forms.Form):

    category_error={'required':u"카테고리는 필수 입니다.",}
    title_error={'required':u"필수 항목 입니다.",}
    intro_line_error={'required':u"필수 항목 입니다.",}
    classtype_error={'required':u"필수 항목 입니다.",}


    category=forms.CharField(error_messages=category_error)
    title=forms.CharField(error_messages=title_error)
    intro_line=forms.CharField(error_messages=intro_line_error)
    classtype=forms.CharField(error_messages=classtype_error)


class T2TeachClassForm(forms.ModelForm):
    category_error={'required':u"카테고리는 필수 입니다.",}
    title_error={'required':u"필수 항목 입니다.",}
    intro_line_error={'required':u"필수 항목 입니다.",}
    classtype_error={'required':u"필수 항목 입니다.",}
    required_error={'required':u"필수 항목 입니다.",}
    url_error={"invalid":u"url주소를 적어주세요."}
    num_error={'required':u"필수 항목 입니다.",
        'invalid':u"숫자만 입력해주세요",}

    category=forms.CharField(error_messages=category_error,required=False)
    title=forms.CharField(error_messages=title_error, required=False)
    intro_line=forms.CharField(error_messages=intro_line_error, required=False)
    classtype=forms.CharField(error_messages=classtype_error, required=False)

    repeat=forms.IntegerField(error_messages=num_error,)
    perhour=forms.IntegerField(error_messages=num_error,)
    weekday=forms.CharField(error_messages=required_error,)
    max_num=forms.IntegerField(error_messages=num_error, )
    min_num=forms.IntegerField(error_messages=num_error)
    startday=forms.DateField(error_messages=required_error)
    deadline=forms.DateField(error_messages=required_error)
    price=forms.IntegerField(error_messages=num_error)
    extra_price=forms.IntegerField(error_messages=num_error)
    video=forms.URLField(required=False, error_messages=url_error)
    descript=forms.CharField(error_messages=required_error)
    curri=forms.CharField(error_messages=required_error)
    notic=forms.CharField(error_messages=required_error)
    addr=forms.CharField(error_messages=required_error)
    addr_detail=forms.CharField(error_messages=required_error)

    class Meta:
        model=T2TeachClass
        fields=('repeat','perhour','weekday','min_num','max_num', 'startday',
                'deadline','price','extra_price','video','descript','curri',
                'notic','addr', 'addr_detail',)

    def save(self, commit=True):
        _sate=self.data.get('state', "")

        _teachpost=super(T2TeachClassForm, self).save(commit=False)
        _teachpost.state=_sate
        _teachpost.save()

        return _teachpost


class T2TutClassForm(forms.ModelForm):
    category_error={'required':u"카테고리는 필수 입니다.",}
    title_error={'required':u"필수 항목 입니다.",}
    intro_line_error={'required':u"필수 항목 입니다.",}
    classtype_error={'required':u"필수 항목 입니다.",}
    required_error={'required':u"필수 항목 입니다.",}
    num_error={'required':u"필수 항목 입니다.",
        'invalid':u"숫자만 입력해주세요",}

    repeat=forms.IntegerField(error_messages=num_error)
    perhour=forms.IntegerField(error_messages=num_error)
    weekday=forms.CharField(error_messages=required_error)
    price=forms.IntegerField(error_messages=num_error)
    extra_price=forms.IntegerField(error_messages=num_error)
    video=forms.CharField(required=False)
    descript=forms.CharField(error_messages=required_error)
    curri=forms.CharField(error_messages=required_error)
    notic=forms.CharField(error_messages=required_error)
    addr=forms.CharField(error_messages=required_error)
    addr_detail=forms.CharField(error_messages=required_error)

    class Meta:
        model=T2TutClass
        fields=('repeat','perhour','weekday','price','extra_price',
                'video','descript','curri','notic','addr', 'addr_detail',)

