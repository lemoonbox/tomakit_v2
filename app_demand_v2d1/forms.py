#coding: utf-8
__author__ = 'moon'
from django import forms

from app_comminfo.models import \
    State, \
    Category
from app_demand_v2d1.models import\
    T2ClassDemand, \
    T2DemandCard, \
    T2DemandPic


class DemandForm(forms.ModelForm):

    GOAL_CHOICE=(
        ('easy&chip', '부담없고 재미있는 수업'),
        ('quality','가격보다는 수업 퀄리티' ),
        ('professional', '창업을 위한 전문 수업' ),
    )
    category_error={'required':u"카테고리는 필수 입니다.",}
    title_error={'required':u"제목은 필수 항목입니다.",}
    descript_error={'required':u"수업은 어떤 방법, 내용으로 진행되길 원하세요?",}
    state_error={'required':u"어떤 지역에서 수업을 찾으세요?",}
    local_error={'required':u"어느 지역의 수업을 찾는지 알려주세요.",}
    weekday_error={'required':u"편한 요일/시간을 알려주세요.",}
    goal_error={'required':u"최소 한개 이상의 수업 목표를 정해주세요.",    }
    mobile_error={'required':u"수업 소식을 문자로 보내드려요. 전화번호를 꼭 입력해주세요.",
                  'invalid':u"숫자로 입력해주세요"}
    min_error={'invalid':u"숫자로 입력해주세요.",}
    max_error={'invalid':u"숫자로 입력해주세요",}

    category=forms.CharField(error_messages=category_error)
    title=forms.CharField(max_length=100, error_messages=title_error)
    descript=forms.CharField(error_messages=descript_error)
    state=forms.CharField(error_messages=state_error)
    local=forms.CharField(max_length=100, error_messages=local_error)
    weekday=forms.CharField(error_messages=weekday_error)
    mobile=forms.IntegerField(error_messages=mobile_error)
    goal=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                            choices=GOAL_CHOICE, error_messages=goal_error)
    min_price=forms.IntegerField(required=False, error_messages=min_error)
    max_price=forms.IntegerField(required=False, error_messages=max_error)

    class Meta:
        model = T2ClassDemand
        fields=('title','descript','local','weekday','min_price','max_price')

    def save(self, commit=True):
        user=self.data['user']
        _category, created=Category.objects.get_or_create(
            category=self.cleaned_data['category'])
        _state, created=State.objects.get_or_create(
            state=self.cleaned_data['state'])
        goals=''
        for goal in self.cleaned_data['goal']:
            goals+="#"+goal
        _demandpost=super(DemandForm, self).save(commit=False)
        _demandpost.user=user
        _demandpost.category=_category
        _demandpost.state=_state
        _demandpost.goal=goals
        _demandpost.save()
        if _demandpost:
            return _demandpost
        return False

    # def modify(self, commite=True):
    #
    #     _category=self.data['category']
    #     _state=self.data['state']
    #     _old_post=self.data["old_post"]
    #     print _old_post
    #
    #     goals=""
    #     for goal in self.cleaned_data['goal']:
    #         goals+="#"+goal
    #     _new_post=super()




class T2DemandCardForm(forms.ModelForm):

    class Meta:
        model=T2DemandCard
        fields=('demand_id','title', 'descript', 'min_price', 'max_price')

    def save(self, commit=True):

        _user=self.data['user']
        _post=self.data['demand_post']
        _category=self.data['category']
        _state=self.data['state']

        _demandcard=super(T2DemandCardForm, self).save(commit=False)
        _demandcard.user=_user
        _demandcard.category=_category
        _demandcard.state=_state
        _demandcard.demand_post=_post
        _demandcard.save()
        if _demandcard:
            return _demandcard
        return False


class T2DemandPicForm(forms.ModelForm):

    image_error={'invalid':"png/jpeg형태의 파일만 업로드 가능합니다."}

    image=forms.ImageField(error_messages=image_error, required=False)

    class Meta:
        model=T2DemandPic
        fields=("image", )


    def is_valid(self):
        valid=super(T2DemandPicForm, self).is_valid()
        if not valid:
            return False
        images=[]
        if self.files:
            images=self.files.getlist('image', "")
        else:
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
        _user=self.data['user']
        _post=self.data['demand_post']
        _card=self.data['demand_card']

        if self.files:
            images=self.files.getlist('image', "")

        imagelist=[]
        if images:
            for file in images:
                print type(file)
                _image=T2DemandPic(user=_user, demand_post=_post,
                                   demand_card=_card, image=file)
                _image.save()
                imagelist.append(_image)
        return imagelist


class CommentForm(forms.Form):

    require_error={"required":u"필수 입력사항입니다."}

    comment=forms.CharField(error_messages=require_error)
    class_ad=forms.CharField(required=False)


class MobliForm(forms.Field):

    mobli_error={"required":u"필수 입력사항입니다.",
                 "invalid":u"숫자만 입력해주세요"}

    mobli1=forms.IntegerField(error_messages=mobli_error)
    mobli2=forms.IntegerField(error_messages=mobli_error)

