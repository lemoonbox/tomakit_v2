from django.contrib import admin
from app_class.models import ClassCategory, \
    PriceTag, \
    ClassInteract, \
    ClassPost, \
    ClassPic, \
    Review, \
    ClassCurri, \
    ClassDetail, \
    CostInfo


##inline classes#####
class C_PicInline(admin.TabularInline):

    fieldsets =((None,
                 {'fields':('user', 'classpost', 'category',
                            'class_photo', 'photo_title',)}
                ),)
    model = ClassPic

    def get_max_num(self, request, obj=None, **kwargs):
        max_num =5

        return max_num
    extra = 0

class ReviewInline(admin.TabularInline):

    fieldsets = ((None,
                  {'fields':('user','classpost','category',
                             'review', 'reviewer_photo','reviewer_name',)}
                 ),)
    model = Review

    def get_max_num(self, request, obj=None, **kwargs):
        max_num =3

        return max_num

class CurriInline(admin.TabularInline):

    fieldsets = ((None,
                  {'fields':('user','classpost','category',
                             'curri_name', 'curri_detail',)}
                 ),)
    model = ClassCurri
    extra = 0

class DetailInline(admin.TabularInline):

    fieldsets = ((None,
                  {'fields':('user','post','category','class_detail')}
    ),)
    model = ClassDetail
    def get_max_num(self, request, obj=None, **kwargs):
        max_num =1

        return max_num


####################

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    fieldsets = [('Cate',{'fields':['category_name', 'is_active',]},)]

class PriceTagAdmin(admin.ModelAdmin):
    list_display = ('price_tag',)
    fieldsets = [('Type',{'fields':['price_tag', 'is_active',]},)]


class C_InteractAdmin(admin.ModelAdmin):
    list_display = ('view_count',)
    fieldsets = [('Count',{'fields':['view_count', 'share_count', 'contact_count',]},)]

class C_PostAdmin(admin.ModelAdmin):

    readonly_fields = ('postinteract',)
    list_filter =['category','user',]
    search_fields = ['user__username', 'title',]

    list_display = ('title', 'price','user', 'day',
                    'contact_tel', 'created_at','updated_at')
    fieldsets = [('Post',{'fields':['user', 'seo_title', 'title','category', 'price',
                                    'price_tag', 'day','time','mem_num', 'video_url',
                                    'need1','need1_detail','need2','need2_detail','contact_tel', 'address',]}),
                 ('postinfo',{'fields':['postinteract','is_active']})]
    inlines = (C_PicInline, ReviewInline, CurriInline, DetailInline)

class C_PicAdmin(admin.ModelAdmin):
    list_filter = ['category', 'classpost__title']
    search_fields = ['classpost__title',]
    list_display = ('id','classpost')
    fieldsets = [(None, {'fields':['user', 'category', 'classpost', 'class_photo', 'photo_title']}),
                   ('Datainfo',{'fields':['is_active']})]

class C_ReviewAdmin(admin.ModelAdmin):
    list_filter = ['category', 'classpost__title']
    search_fields = ['classpost__title',]
    list_display = ('id','classpost')
    fieldsets = [(None, {'fields':['user', 'category', 'classpost', 'review',
                                   'reviewer_photo', 'reviewer_name']}),
                   ('Datainfo',{'fields':['is_active']})]

class C_CurriAdmin(admin.ModelAdmin):
    list_filter = ['category', 'classpost__title']
    search_fields = ['classpost__title',]
    list_display = ('id','classpost')
    fieldsets = [(None, {'fields':['user', 'category', 'classpost',
                                   'curri_name', 'curri_detail']}),
                   ('Datainfo',{'fields':['is_active']})]

class C_DetailAdmin(admin.ModelAdmin):
    list_filter = ['category',]
    search_fields = ['post__title',]
    list_display = ('id','post')
    fieldsets = [(None, {'fields':['user', 'category', 'post', 'class_detail']}),
                 ('Datainfo',{'fields':['is_active']})]

class C_CostInfoAdmin(admin.ModelAdmin):
    search_fields = ['classpost__title',]
    list_display = ('id','classpost', 'apply_url',)
    fieldsets = [(None, {'fields':['classpost', 'apply_url']}),]



# class TestAdmin(admin.ModelAdmin):
#     pass

# admin.site.register(PriceTag, PriceTagAdmin)
# admin.site.register(ClassCategory, CategoryAdmin)
# admin.site.register(ClassInteract, C_InteractAdmin)
# admin.site.register(ClassPost, C_PostAdmin)
# admin.site.register(ClassPic, C_PicAdmin)
# admin.site.register(ClassDetail, C_DetailAdmin)
# admin.site.register(Review,C_ReviewAdmin)
# admin.site.register(ClassCurri,C_CurriAdmin)
# admin.site.register(CostInfo, C_CostInfoAdmin)