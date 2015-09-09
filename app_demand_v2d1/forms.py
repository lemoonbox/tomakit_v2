#coding: utf-8
__author__ = 'moon'
from django import forms


class DemandForm(forms.Form):

    GOAL_CHOICE=(
        ('easy&chip', u'부담없고 재미있는 수업'),
        ('quality',u'가격보다는 수업 퀄리티' ),
        ('professional', u'창업을 위한 전문 수업' ),
    )

    category_error={'required':u"카테고리는 필수 입니다.",}
    title_error={'required':u"좋은 제목으로 사람들이 줄서게 만들어 보세요:)",}
    descript_error={'required':u"수업은 어떤 방법, 내용으로 진행되길 원하세요?",}
    state_error={'required':u"어떤 지역에서 수업을 찾으세요?",}
    local_error={'required':u"어느 지역의 수업을 찾는지 알려주세요.",}
    weekday_error={'required':u"편한 요일/시간을 알려주세요.",}
    goal_error={'required':u"어떤 종류의 수업을 찾으세요?",    }
    min_error={'invalid':u"숫자로 입력해주세요.",}
    max_error={'invalid':u"숫자로 입력해주세요",}

    category=forms.CharField(error_messages=category_error)
    title=forms.CharField(max_length=100, error_messages=title_error)
    descript=forms.CharField(error_messages=descript_error)
    state=forms.CharField(error_messages=state_error)
    local=forms.CharField(max_length=100, error_messages=local_error)
    weekday=forms.CharField(error_messages=weekday_error)
    #goal=forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, error_messages=goal_error)

    min_price=forms.IntegerField(required=False, error_messages=min_error)
    max_price=forms.IntegerField(required=False, error_messages=max_error)


