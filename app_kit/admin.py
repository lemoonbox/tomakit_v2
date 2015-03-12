from django.contrib import admin
from app_kit.models import Kit_Post, Kit_Detailm, Kit_Photo

class KitPostAdmin(admin.ModelAdmin):
    list_filter =['user', 'category', 'title']
    search_fields = ['user', 'category', 'title']

    list_display = ('title','category','price','user', 'contact_tel', 'created_at', 'updated_at')
    fieldsets = [('KitPost',{'fields':['user', 'category', 'title', 'price',
                                         'describe', 'contact_tel', 'address']}),
        ('Datainfo',{'fields':['is_active']})]


class KitPhotoAdmin(admin.ModelAdmin):
    list_filter = ['user', 'kit_post__id', 'kit_post__title']
    search_fields = ['user', 'kit_post__title']

    fieldsets = [(None, {'fields':['user', 'kit_post', 'kit_photo']})]

class KitDetailAdmin(admin.ModelAdmin):
    list_filter = ['user', 'kit_post__id', 'kit_post__title']
    search_fields = ['user','kit_post__id', 'kit_post__title']

    fieldsets = [(None, {'fields':['user', 'kit_post', 'kit_detail']})]



admin.site.register(Kit_Photo, KitPhotoAdmin)
admin.site.register(Kit_Detailm, KitDetailAdmin)
admin.site.register(Kit_Post, KitPostAdmin)