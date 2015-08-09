#coding: utf-8
from django.contrib import admin
from app_user.models import UserProfile, HostProfile
# Register your models here.



class ProfileAdmin(admin.ModelAdmin):
    list_display = ('djgouser', 'created_at')

    fieldsets = [("AccountInfo",{'fields':['djgouser', 'propic',
                                            'inter_oneline', 'inter_start','inter_pic',
                                            'inter_url', 'mailcnfirm', 'is_activate',]})]


admin.site.register(UserProfile, ProfileAdmin)

class HostProfileAdmin(admin.ModelAdmin):

    list_display = ('djgouser', 'hosttype','mobile')

    fieldsets = [('HostInfo', {'fields':['djgouser', 'hosttype','mobile']})]


admin.site.register(HostProfile, HostProfileAdmin)