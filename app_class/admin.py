from django.contrib import admin
from app_class.models import ClassPost, ClassPic, ClassDetail

class ClassPostAdmin(admin.ModelAdmin):
    list_filter =['user', 'category', 'title', 'lessonday', 'created_at', 'updated_at']
    search_fields = ['user', 'category', 'title']

    list_display = ('title','category','price','user', 'lessonday',
                    'contact_tel', 'created_at','updated_at')
    fieldsets = [('ClassPost',{'fields':['user', 'category', 'title', 'price',
                                         'describe', 'lessonday', 'start_time', 'end_time',
                                         'minimum', 'maximum', 'contact_tel', 'address']}),
                 ('Datainfo',{'fields':['is_active']})]

class ClassPicAdmin(admin.ModelAdmin):
    list_filter = ['user', 'class_post__id', 'class_post__title']
    search_fields = ['user', 'category', 'class_post__title']

    fieldsets = [(None, {'fields':['user', 'class_post', 'class_photo']})]

class ClassDetailAdmin(admin.ModelAdmin):
    list_filter = ['user', 'class_post__id', 'class_post__title']
    search_fields = ['user', 'category', 'class_post__id', 'class_post__title']

    fieldsets = [(None, {'fields':['user', 'class_post', 'class_detail']})]


admin.site.register(ClassPost, ClassPostAdmin)
admin.site.register(ClassPic, ClassPicAdmin)
admin.site.register(ClassDetail, ClassDetailAdmin)