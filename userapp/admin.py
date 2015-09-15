from django.contrib import admin
from userapp.models import Profile, SellerInfo

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_filter =['created_at', 'email']
    search_fields = ['email','nick_name']
    list_display = ('user','email','nick_name','email_confirm', 'created_at', "updated_at")
    fieldsets = [('Identity',{'fields':['user', 'email', 'nick_name', 'pro_photo']}),
        ('Datainfo',{'fields':['email_confirm']})]



class SellerInfoAdmin(admin.ModelAdmin):
    search_fields = ['user']
    list_display=('user', 'special','intro', )
    fieldsets = [('SellerInfo', {'fields':['user', 'intro', 'special',]}),
                 ]
# admin.site.register(Profile, ProfileAdmin)
#
# admin.site.register(SellerInfo, SellerInfoAdmin)