from django.contrib import admin
from app_user_v2d1.models import \
    T2Profile, \
    T2HostProfile
# Register your models here.



class T2ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'mail_conf','mobli','created_at','updated_at')

    fieldsets = [("AccountInfo",{'fields':['user', 'mail_conf','pro_pic',
                                            'intro_line', 'mobli1','mobli2',
                                            'mobli','mobli_able',
                                            'mobli_conf', 'is_activate']})]

admin.site.register(T2Profile, T2ProfileAdmin),

class T2HostProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'intro_self','created_at','updated_at')

    fieldsets = [("AccountInfo",{'fields':['user', 'intro_self','intro_video',
                                            'intro_pic', 'shop_addr',
                                            'shop_addr_detail','hosttype','is_active']})]

admin.site.register(T2HostProfile, T2HostProfileAdmin),