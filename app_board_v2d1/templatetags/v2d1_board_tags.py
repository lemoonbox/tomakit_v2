#coding:utf-8
__author__ = 'moon'


from django import template
import datetime
register = template.Library()

@register.filter(name="cate2han")
def cate2han(valu, argu=None):
    if valu == "cate_1":
        return  u"공예"
    elif valu =="cate_2":
        return u"아트"
    elif valu =="cate_3":
        return u"푸드"
    else :
        return u"기타"

@register.filter(name="state2han")
def state2han(valu, argu=None):
    if valu == "zone_1":
        return  u"서울"
    elif valu =="zone_2":
        return u"경기.인천"
    elif valu =="zone_3":
        return u"부산"
    else :
        return u"다른 지역"

@register.filter(name="d_day_count")
def d_day_count(valu, argu=None):
    today=datetime.date.today()
    timeoff=today-valu
    return timeoff.days

@register.filter(name="classtype2han")
def classtype2han(valu, argu=None):
    if valu == "tutclass":
        return u"상시 모집"
    else:
        day=d_day_count(valu)
        if day<0:
            return "마감"+str(-day)+"일전"
        else:
            return "수업 마감"


@register.filter(name="goaltag2han")
def goaltag2han(valu, argu=None):
    goallist=valu.split("#")
    hantags=""
    for goal in goallist:
        if goal == "easy&chip":
            hantags+=u" #부담없고 재미있는 수업"
        elif goal == "quality":
            hantags+=u" #가격보다는 수업 퀄리티"
        elif goal == "professional":
            hantags+=u" #창업을 위한 전문 수업"

    return hantags


@register.filter(name="classtype2han")
def class_status(valu, argu=None):
    if valu == "True":
        return "SOLD OUT"
    else:
        pass
