from django.contrib import admin
from app_demand_v2d1.models import \
    T2ClassDemand, \
    T2DemandCard

# Register your models here.

class T2ClassDemandAdmin(admin.ModelAdmin):

    list_display=('user', 'id','title','category',
                  'local','goal','inline_cnt','created_at','updated_at')
    fieldsets=[("DemandInfo",{'fields':['user','category','title',
                                        'descript','state','local',
                                        'weekday','goal','inline_cnt',
                                        'inline_users','min_price','max_price',
                                        'is_active']})]
admin.site.register(T2ClassDemand, T2ClassDemandAdmin)


class T2DemandCardAdmin(admin.ModelAdmin):

    list_display=('user', 'demand_id','title','category',
                  'state','inline_cnt','created_at','updated_at')
    fieldsets=[("DemandInfo",{'fields':['user','demand_id', 'demand_post',
                                        'category','title','descript',
                                        'state','inline_cnt','inline_users',
                                        'min_price','max_price','is_active']})]
admin.site.register(T2DemandCard, T2DemandCardAdmin)