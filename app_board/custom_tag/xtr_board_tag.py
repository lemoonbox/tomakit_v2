#coding : utf-8
__author__ = 'moon'


from django import template

register = template.Library()

@register.filter()
def cate2han(valu, argu):
    if valu == "leather":
        return
    elif valu =="calligraphy":
        return
    elif valu =="flower":
        return
    elif valu =="dyeing":
        return
    elif valu =="pottery":
        return
    elif valu =="home-living":
        return
    elif valu =="sewing":
        return
    elif valu =="etc":
        return
    elif valu =="woodwork":
        return
    elif valu =="art":
        return
    elif valu =="toreutics":
        return
    elif valu =="knot":
        return
    elif valu =="knit":
        return
    elif valu =="bake":
        return
    elif valu =="cosmetics":
        return