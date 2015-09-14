#coding: utf-8
__author__ = 'moon'
from django import forms

from app_class_v2d1.models import \
    T2TutClass, \
    T2TeachClass,\
    T2ClassPic,\
    T2ClassCard



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
    url_error={"invalid":u"url주소를 적어주세요."}


    repeat=forms.IntegerField(error_messages=num_error)
    perhour=forms.IntegerField(error_messages=num_error)
    weekday=forms.CharField(error_messages=required_error)
    price=forms.IntegerField(error_messages=num_error)
    extra_price=forms.IntegerField(error_messages=num_error)
    video=forms.URLField(required=False, error_messages=url_error)
    descript=forms.CharField(error_messages=required_error)
    curri=forms.CharField(error_messages=required_error)
    notic=forms.CharField(error_messages=required_error)
    addr=forms.CharField(error_messages=required_error)
    addr_detail=forms.CharField(error_messages=required_error)

    class Meta:
        model=T2TutClass
        fields=('repeat','perhour','weekday','price','extra_price',
                'video','descript','curri','notic', 'addr', 'addr_detail',)

    def save(self, commit=True):
        _sate=self.data.get('state', "")

        _tutpost=super(T2TutClassForm, self).save(commit=False)
        _tutpost.state=_sate
        _tutpost.save()

        return _tutpost


class T2ClassCardForm(forms.ModelForm):

    class Meta:
        model=T2ClassCard
        fields=('classtype', 'class_id','title', 'intro_line','repeat',
                'perhour', 'price', 'extra_price')

    def save(self, commit=True):
        _user=self.data.get('user', "")
        _teach_post=self.data.get('teach_post',"")
        _tut_post=self.data.get('tut_post',"")
        _category=self.data.get('category', "")
        _state=self.data.get('state', "")

        _card=super(T2ClassCardForm, self).save(commit=False)
        _card.user=_user
        _card.category=_category
        _card.state=_state

        if _teach_post:
            _card.teach_post=_teach_post
        else:
            _card.tut_post=_tut_post
        _card.save()
        if _card:
            return _card
        return False


class T2ClassPicForm(forms.ModelForm):

    image_error={'invalid':"png/jpeg형태의 파일만 업로드 가능합니다."}

    image=forms.ImageField(error_messages=image_error, required=False)

    class Meta:
        model=T2ClassPic
        fields=("image", )


    def is_valid(self):
        valid=super(T2ClassPicForm, self).is_valid()

        if not valid:
            return False

        images=[]
        if self.files:
            images=self.files.getlist('image', "")
        else :
            return False
        if images:
            for file in images:
                if file.content_type == "image/png" or \
                                file.content_type == "image/jpeg":
                    valid=True
                else :
                    self.add_error("image", "png/jpeg형태의 파일만 업로드 가능합니다.")
                    return False
        return valid


    def savefiles(self, commit=True):
        _user=self.data.get('user', "")
        _teach_post=self.data.get('teach_post', "")
        _tut_post=self.data.get('tut_post', "")
        _class_card=self.data.get('class_card', "")


        if self.files:
            images=self.files.getlist('image', "")

        imagelist=[]
        if images:
            for file in images:
                if _teach_post:
                    _image=T2ClassPic(user=_user, teach_post=_teach_post,
                                       class_card=_class_card, image=file)
                    _image.save()
                    imagelist.append(_image)
                else :
                    _image=T2ClassPic(user=_user, tut_post=_tut_post,
                   class_card=_class_card, image=file)
                    _image.save()
                    imagelist.append(_image)

        return imagelist
