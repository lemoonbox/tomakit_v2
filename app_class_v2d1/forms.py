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
    num_error={'required':u"필수 항목 입니다.",
        'invalid':u"숫자만 입력해주세요",}

    category=forms.CharField(error_messages=category_error)
    title=forms.CharField(error_messages=title_error)
    intro_line=forms.CharField(error_messages=intro_line_error)
    classtype=forms.CharField(error_messages=classtype_error)
    repeat=forms.IntegerField(error_messages=num_error,)
    perhour=forms.IntegerField(error_messages=num_error,)
    weekday=forms.CharField(error_messages=required_error,)
    max_num=forms.IntegerField(error_messages=num_error, )
    min_num=forms.IntegerField(error_messages=num_error)
    startday=forms.DateField(error_messages=required_error)
    deadline=forms.DateField(error_messages=required_error)
    price=forms.IntegerField(error_messages=num_error)
    extra_price=forms.IntegerField(error_messages=num_error)
    video=forms.CharField(required=False)
    descript=forms.CharField(error_messages=required_error)
    curri=forms.CharField(error_messages=required_error)
    notic=forms.CharField(error_messages=required_error)
    addr=forms.CharField(error_messages=required_error)
    addr_detail=forms.CharField(error_messages=required_error)

    class Meta:
        model=T2TeachClass
        fields=('title','intro_line','repeat','perhour','weekday',
                'min_num','max_num', 'startday', 'deadline','price',
                'extra_price','video','descript','curri','notic','addr', 'addr_detail',)

    def save(self, commit=True):
        _user=self.data['user']
        _category=self.data.get('category', "")
        _sate=self.data.get('state', "")

        _teachpost=super(T2TeachClassForm, self).save(commit=False)
        _teachpost.user=_user
        _teachpost.category=_category
        if _sate:
            print "state nok"





class T2TutClassForm(forms.ModelForm):
    category_error={'required':u"카테고리는 필수 입니다.",}
    title_error={'required':u"필수 항목 입니다.",}
    intro_line_error={'required':u"필수 항목 입니다.",}
    classtype_error={'required':u"필수 항목 입니다.",}
    required_error={'required':u"필수 항목 입니다.",}
    num_error={'required':u"필수 항목 입니다.",
        'invalid':u"숫자만 입력해주세요",}

    category=forms.CharField(error_messages=category_error)
    title=forms.CharField(error_messages=title_error)
    intro_line=forms.CharField(error_messages=intro_line_error)
    classtype=forms.CharField(error_messages=classtype_error)
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
        fields=('classtype','title','intro_line','repeat','perhour','weekday',
                'price','extra_price','video','descript','curri','notic',
                'addr', 'addr_detail',)

