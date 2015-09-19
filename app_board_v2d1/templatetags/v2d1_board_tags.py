#coding:utf-8
__author__ = 'moon'


from django import template
import datetime
register = template.Library()

@register.filter(name="cate2han")
def cate2han(valu, argu=None):
    if valu == "leather":
        return  u"가죽공예"
    elif valu =="calligraphy":
        return u"캘리그라피"
    elif valu =="flower":
        return u"플라워/디퓨저"
    elif valu =="dyeing":
        return u"천연염색"
    elif valu =="pottery":
        return u"도자기공예"
    elif valu =="home_living":
        return u"Home&Living"
    elif valu =="sewing":
        return u"미싱/옷만들기"
    elif valu =="etc":
        return u"기타"
    elif valu =="woodwork":
        return u'목공예'
    elif valu =="art":
        return u"미술"
    elif valu =="toreutics":
        return u"금속공예/악세사리"
    elif valu =="knot":
        return u"매듭"
    elif valu =="knit":
        return u"뜨개질"
    elif valu =="bake":
        return u"베이킹/쿠킹"
    elif valu =="cosmetics":
        return u"천연화장품/비누"
    else :
        return u"ALL"

@register.filter(name="state2han")
def state2han(valu, argu=None):
    if valu == "seoul":
        return  u"서울"
    elif valu =="incheon_gyeonggi":
        return u"인천/경기"
    elif valu =="busan_ulsan_gyeongnam":
        return u"부산/울산/경남"
    elif valu =="daegu_gyeongbuk":
        return u"대구/경북"
    elif valu =="daejeon_chungcheong":
        return u"대전/충청"
    elif valu =="gwangju_jeonla":
        return u"광주/전라"
    elif valu =="gangwon":
        return u"강원"
    elif valu =="jeju":
        return u"제주"
    elif valu =="etc":
        return u'기타'
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
        return u"바로 신청 가능"
    else:
        return d_day_count(valu)

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
            hantags+=" #창업을 위한 전문 수업"

    return hantags
