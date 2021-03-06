#coding: utf-8
__author__ = 'moon'
from django import forms

from app_class_v2d1.models import \
    T2TutClass, \
    T2TeachClass,\
    T2ClassPic,\
    T2ClassCard, \
    T2ClassReview, \
    T2CardPic
from utils.utils import shard_url_picker, handle_uploaded_image,\
    hfix_uploaded_image


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
    addr_error={"required": u"주소를 입력해주세요."}
    addr_detail_error={"required": u"상세 주소를 입력해주세요."}

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
    video=forms.CharField(max_length=250,required=False)
    descript=forms.CharField(error_messages=required_error)
    curri=forms.CharField(error_messages=required_error)
    notic=forms.CharField(error_messages=required_error)
    locality=forms.CharField(required=False)
    area_1=forms.CharField(required=False)
    sublocal_1=forms.CharField(required=False)
    sublocal_2=forms.CharField(required=False)
    sublocal_4=forms.CharField(required=False)
    addr=forms.CharField(error_messages=addr_error)
    addr_detail=forms.CharField(error_messages=addr_detail_error)

    class Meta:
        model=T2TeachClass
        fields=('repeat','perhour','weekday','min_num','max_num', 'startday',
                'deadline','price','extra_price','video','descript','curri',
                'notic','locality', 'area_1', 'sublocal_1','sublocal_2','sublocal_4',
                'addr', 'addr_detail',)

    def save(self, commit=True):
        _sate=self.data.get('state', "")
        video_url=self.data.get('video', "").encode("utf-8")

        _teachpost=super(T2TeachClassForm, self).save(commit=False)
        _teachpost.state=_sate
        _teachpost.video=shard_url_picker(video_url)
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
    addr_error={"required": u"주소를 입력해주세요."}
    addr_detail_error={"required": u"상세 주소를 입력해주세요."}

    repeat=forms.IntegerField(error_messages=num_error)
    perhour=forms.IntegerField(error_messages=num_error)
    weekday=forms.CharField(error_messages=required_error)
    price=forms.IntegerField(error_messages=num_error)
    extra_price=forms.IntegerField(error_messages=num_error)
    video=forms.CharField(max_length=250, required=False)
    descript=forms.CharField(error_messages=required_error)
    curri=forms.CharField(error_messages=required_error)
    notic=forms.CharField(error_messages=required_error)
    locality=forms.CharField(required=False)
    area_1=forms.CharField(required=False)
    sublocal_1=forms.CharField(required=False)
    sublocal_2=forms.CharField(required=False)
    sublocal_4=forms.CharField(required=False)
    addr=forms.CharField(error_messages=addr_error)
    addr_detail=forms.CharField(error_messages=addr_detail_error)

    class Meta:
        model=T2TutClass
        fields=('repeat','perhour','weekday','price','extra_price',
                'locality', 'area_1', 'sublocal_1','sublocal_2','sublocal_4',
                'video','descript','curri','notic', 'addr', 'addr_detail',)

    # def is_valid(self):
    #     valid=super(T2TutClassForm, self).is_valid()
    #     print valid
    #     if valid:
    #         addr=self.data.get("addr", "")
    #         if addr:
    #             print addr
    #             print "is_addr ok"
    #             return True
    #     else:
    #         self.add_error("addr", "주소를 입력해주세요.")
    #
    #     return valid

    def save(self, commit=True):
        _sate=self.data.get('state', "")
        video_url=self.data.get('video', "").encode("utf-8")


        _tutpost=super(T2TutClassForm, self).save(commit=False)
        _tutpost.state=_sate
        _tutpost.video=shard_url_picker(video_url)
        _tutpost.save()

        return _tutpost


class T2ClassCardForm(forms.ModelForm):

    class Meta:
        model=T2ClassCard
        fields=('classtype', 'class_id','title', 'intro_line','repeat',
                'locality', 'area_1', 'sublocal_1','sublocal_2','sublocal_4',
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

    image_error={'invalid':"png/jpeg형태의 파일만 업로드 가능합니다.",
                 'requeir':"한장 이상 사진을 입력해주세요."}

    image=forms.ImageField(error_messages=image_error, required=False)

    class Meta:
        model=T2ClassPic
        fields=("image", )

    def is_valid(self):
        valid=super(T2ClassPicForm, self).is_valid()

        images=[]
        if valid and self.files:
            images=self.files.getlist('image', "")
            for file in images:
                if not file.content_type == "image/png" and \
                                not file.content_type == "image/jpeg":
                    self.add_error("image", "png/jpeg형태의 파일만 업로드 가능합니다.")
                    return False
        else:
            self.add_error("image", "한장 이상 사진을 입력해주세요")
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
                file=handle_uploaded_image(file, 1140, 820)[1]
                if _teach_post:
                    _image=T2ClassPic(user=_user, teach_post=_teach_post,
                                       class_card=_class_card, image=file)
                    _image.save()
                    imagelist.append(_image)
                elif _tut_post:
                    _image=T2ClassPic(user=_user, tut_post=_tut_post,
                   class_card=_class_card, image=file)
                    _image.save()
                    imagelist.append(_image)
        return imagelist

class T2CardPicForm(forms.ModelForm):

    image_error={'invalid':"png/jpeg형태의 파일만 업로드 가능합니다."}
    image=forms.ImageField(error_messages=image_error, required=False)

    class Meta:
        model=T2CardPic
        fields=("image", )

    def save_img(self, commit=True):
        _user=self.data.get('user', "")
        _class_card=self.data.get('class_card', "")

        if self.files:
            images=self.files.getlist('card_img', "")

        imagelist=[]
        if images:
            for file in images:
                card_img=handle_uploaded_image(file, 504, 336)[1]
                _cardimage=T2CardPic(user=_user, class_card=_class_card,
                                     image=card_img)
                _cardimage.save()
        return card_img


class T2ReviewForm(forms.ModelForm):

    review_error={"required":u"필수 입력사항입니다.",}
    grade_error={"required":u"필수 입력사항입니다.",
                 "invalid":u'숫자만 가능 합니다.'}

    review=forms.CharField(error_messages=review_error)
    grade=forms.IntegerField(error_messages=grade_error)

    class Meta:
        model=T2ClassReview
        fields=('review', 'grade')

    def is_valid(self):
        valid = super(T2ReviewForm, self).is_valid()
        _user=self.data.get("user", "")
        _post=self.data.get("post", "")
        classtype=self.data.get("classtype", "")


        if valid and _user:
            _review_exist=""
            if classtype =="tut_class":
                _review_exist=T2ClassReview.objects.filter(
                    tut_post=_post,user=_user, is_active=True).exists()
            else:
                _review_exist=T2ClassReview.objects.filter(
                    teach_post=_post,user=_user, is_active=True).exists()
            if _review_exist:
                self.add_error("review",u"리뷰는 1인당 1개만 입력 가능합니다.")
                return False
            else :
                return True

        return False
