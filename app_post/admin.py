from django.contrib import admin
from app_post.models import Post, PostCategory, PostType, PostDetail, PostPic

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    fieldsets = [('Cate',{'fields':['category_name', 'is_active',]},)]

class TypeAdmin(admin.ModelAdmin):
    list_display = ('type_name',)
    fieldsets = [('Type',{'fields':['category_name', 'is_active',]},)]

class PostAdmin(admin.ModelAdmin):
    list_filter =['category','type', 'lessonday',]
    search_fields = ['user__username', 'title', 'describe',]

    list_display = ('title', 'price','user', 'lessonday',
                    'contact_tel', 'created_at','updated_at')
    fieldsets = [('Post',{'fields':['user', 'category', 'type', 'title', 'price',
                                    'describe', 'lessonday', 'start_time', 'end_time',
                                    'minimum', 'maximum', 'contact_tel', 'address']}),
                 ('Datainfo',{'fields':['is_active']})]

class PicAdmin(admin.ModelAdmin):
    list_filter = ['category', 'type']
    search_fields = ['post__title',]
    list_display = ('id','post')
    fieldsets = [(None, {'fields':['user', 'category', 'type', 'post', 'post_photo']}),
                   ('Datainfo',{'fields':['is_active']})]

class DetailAdmin(admin.ModelAdmin):
    list_filter = ['category', 'type',]
    search_fields = ['post__title',]
    list_display = ('id','post')
    fieldsets = [(None, {'fields':['user', 'category', 'type', 'post', 'post_detail']}),
                 ('Datainfo',{'fields':['is_active']})]

admin.site.register(PostType, TypeAdmin)
admin.site.register(PostCategory, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostPic, PicAdmin)
admin.site.register(PostDetail, DetailAdmin)
