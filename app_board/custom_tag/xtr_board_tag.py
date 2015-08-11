#coding : utf-8
__author__ = 'moon'


from django import template

register = template.Library()

@register.filter()
def cate2han(valu, argu):
    if valu == ""