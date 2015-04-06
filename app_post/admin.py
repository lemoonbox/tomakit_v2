# from django.contrib import admin
# from app_post.models import Post, PostCategory, PostType, PostDetail, PostPic
#
#
# class PostAdmin(admin.ModelAdmin):
#     list_filter =['user', 'category','type' 'title', 'lessonday']
#     search_fields = ['user', 'category','type' 'title']
#
#     list_display = ('title','category','type', 'price','user', 'lessonday',
#                     'contact_tel', 'created_at','updated_at')
#     fieldsets = [('Post',{'fields':['user', 'category', 'type', 'title', 'price',
#                                     'describe', 'lessonday', 'start_time', 'end_time',
#                                     'minimum', 'maximum', 'contact_tel', 'address']}),
#                  ('Datainfo',{'fields':['is_active']})]
#
# class PicAdmin(admin.ModelAdmin):
#     list_filter = ['user', 'post__id', 'post__title']
#     search_fields = ['user', 'category', 'type', 'post__title']
#
#     fieldsets = [(None, {'fields':['user', 'category', 'type', 'post', 'post_photo']})]
#
# class DetailAdmin(admin.ModelAdmin):
#     list_filter = ['user', 'post__id', 'post__title']
#     search_fields = ['user', 'category', 'type', 'post__id', 'post__title']
# 
#     fieldsets = [(None, {'fields':['user', 'category', 'type', 'post', 'detail']})]
#
#
# admin.site.register(Post, PostAdmin)
# admin.site.register(PostPic, PicAdmin)
# admin.site.register(PostDetail, DetailAdmin)
