#coding: utf-8
__author__ = 'moon'
from django import forms

from app_comminfo.models import \
    State, \
    Category
from app_demand_v2d1.models import\
    T2ClassDemand


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
    mobile_error={'required':u"수업 견적을 문자로 보내드립니다. 전화번호를 꼭 입력해주세요.",
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
            goals+=goal+"-----"

        _demandpost=super(DemandForm, self).save(commit=False)
        _demandpost.user=user
        _demandpost.category=_category
        _demandpost.state=_state
        _demandpost.goal=goals
        _demandpost.save()

        return _demandpost