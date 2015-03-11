__author__ = 'moon'

from django import template

register = template.Library()


@register.filter()
def cut(value, arg):
    return value

@register.filter()
def lower(value): # Only one argument.
    """Converts a string into all lowercase"""
    return value.lower()


@register.filter
def classname(obj):
    classname = obj.__class__.__name__
    return classname

@register.filter
def big_mid(obj):
    print obj
    num = int(obj)
    check = num%3

    return check