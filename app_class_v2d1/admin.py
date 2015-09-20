from django.contrib import admin
from app_class_v2d1.models import \
    T2ClassCard, \
    T2TeachClass, \
    T2TutClass, \
    T2ClassReview, \
    T2ClassPic
# Register your models here.

class T2TeachClassAdmin(admin.ModelAdmin):

    list_display=('title', 'id', 'repeat','perhour', 'price', 'extra_price')
    fieldsets=[('Redcord',{'fields':['user', 'category','classtype', 'title', 'intro_line',
                                     'repeat', 'perhour', 'weekday', 'max_num',
                                     'min_num', 'startday', 'deadline', 'price',
                                     'extra_price', 'video', 'descript', 'curri',
                                     'notic', 'state', 'addr', 'addr_detail',
                                     'wr_done', 'deadline_over', 'is_open', 'is_active',],})]

admin.site.register(T2TeachClass, T2TeachClassAdmin)

class T2TutClassAdmin(admin.ModelAdmin):

    list_display=('title', 'id', 'repeat','perhour', 'price', 'extra_price')
    fieldsets=[('Redcord',{'fields':['user', 'category','classtype', 'title', 'intro_line',
                                     'repeat', 'perhour', 'weekday',  'price',
                                     'extra_price', 'video', 'descript', 'curri',
                                     'notic', 'state', 'addr', 'addr_detail',
                                     'wr_done', 'deadline_over', 'is_open', 'is_active',],})]

admin.site.register(T2TutClass, T2TutClassAdmin)


class T2ClassCardAdmin(admin.ModelAdmin):

    list_display=('title', 'id', 'repeat','perhour', 'price', 'extra_price')
    fieldsets=[('Redcord',{'fields':['user', 'category','state', 'teach_post', 'tut_post',
                                     'classtype', 'class_id', 'title', 'intro_line',
                                     'repeat', 'perhour', 'price', 'extra_price',
                                     'pop_point','wr_done', 'deadline_over', 'is_open', 'is_active'],})]

admin.site.register(T2ClassCard, T2ClassCardAdmin)

class T2ReviewAmdin(admin.ModelAdmin):
    list_display=('review', 'id', 'user','grade','host_user','teach_post', 'tut_post')
    fieldsets=[('Redcord',{'fields':['user', 'host_user','teach_post', 'tut_post', 'grade',
                                     'review', 'image', 'is_active'],})]

admin.site.register(T2ClassReview, T2ReviewAmdin)
