#coding:utf-8
__author__ = 'moon'


from django import template
import datetime
register = template.Library()

@register.filter(name="cate2han")
def cate2han(valu, argu=None):
    if valu == "cate_1":
        return  u"가죽공예"
    elif valu =="cate_2":
        return u"플라워아트"
    elif valu =="cate_3":
        return u"전통공예/한복"
    elif valu =="cate_4":
        return u"목공예"
    elif valu =="cate_5":
        return u"금속공예/매듭"
    elif valu =="cate_6":
        return u"재봉틀/뜨개질"
    elif valu =="cate_7":
        return u"캘리그라피"
    elif valu =="cate_8":
        return u"그리기"
    elif valu =="cate_9":
        return u'베이킹/요리'
    elif valu =="cate_10":
        return u"화장품/향기"
    elif valu =="cate_11":
        return u"기타"
    else :
        return u"ALL"

@register.filter(name="state2han")
def state2han(valu, argu=None):
    if valu == "zone_1":
        return  u"도봉/성북/동대문..."
    elif valu =="zone_2":
        return u"은평/마포/서대문..."
    elif valu =="zone_3":
        return u"종로/중구/용산..."
    elif valu =="zone_4":
        return u"양천/영등포/동작.."
    elif valu =="zone_5":
        return u"송파/강남/서초..."
    elif valu =="zone_6":
        return u"수원/안산/안양..."
    elif valu =="zone_7":
        return u"성남/남양주/용인..."
    elif valu =="zone_8":
        return u"파주/의정부/고양..."
    elif valu =="zone_9":
        return u'인천/부천'
    else :
        return u"ALL"

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
