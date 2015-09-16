from django.contrib import admin
from app_demand_v2d1.models import \
    T2ClassDemand, \
    T2DemandCard, \
    T2DemandPic, \
    T2DemandCmt

# Register your models here.


class T2DemandPicLine(admin.TabularInline):

    fieldsets =(("Images",
                 {'fields':('user', 'demand_post', 'demand_card',
                            'image', 'is_active',)}
                ),)
    model = T2DemandPic

    def get_max_num(self, request, obj=None, **kwargs):
        max_num =3

        return max_num
    extra = 0

class T2ClassDemandAdmin(admin.ModelAdmin):

    list_display=('title','user', 'id','category',
                  'local','goal','inline_cnt','created_at','updated_at')
    fieldsets=[("DemandInfo",{'fields':['user','category','title',
                                        'descript','state','local',
                                        'weekday','goal','inline_cnt',
                                        'inline_users','min_price','max_price',
                                        'is_active']})]
    inlines = (T2DemandPicLine,)
admin.site.register(T2ClassDemand, T2ClassDemandAdmin)


class T2DemandCardAdmin(admin.ModelAdmin):

    list_display=('title','user', 'demand_id','category',
                  'state','inline_cnt','created_at','updated_at')
    fieldsets=[("DemandInfo",{'fields':['user','demand_id', 'demand_post',
                                        'category','title','descript',
                                        'state','inline_cnt','inline_users',
                                        'min_price','max_price','is_active']})]
admin.site.register(T2DemandCard, T2DemandCardAdmin)

class T2DemandCmtAdmin(admin.ModelAdmin):
    list_display=('comment','user', 'class_ad','created_at','updated_at')
    fieldsets=[("CmtInfo",{'fields':['user','demand_post', 'comment',
                                        'class_ad','is_active']})]

admin.site.register(T2DemandCmt, T2DemandCmtAdmin)
