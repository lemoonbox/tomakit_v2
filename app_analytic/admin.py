from django.contrib import admin
from app_analytic.models import FB_item_code, SearchRecord, Read_cnt
# Register your models here.

class FB_item_codeAdmin(admin.ModelAdmin):

    search_fields = ['tutpost','teachpost','demandpost']

    list_display = ('tutpost','teachpost','demandpost')
    fieldsets = [('Post',{'fields':['buy_C','read_C', 'tutpost','teachpost','demandpost']}),
                 ('postinfo',{'fields':['is_active',]})]

class SearchRecordAdmin(admin.ModelAdmin):

    list_display=('target_cate', 'target_state', 'target_word')
    fieldsets=[('Redcord',{'fields':['target_cate', 'target_state',
                                     'target_word', 'is_active']})]

class ReadCntAdimn(admin.ModelAdmin):

    list_display=('target_tut', 'target_teach','target_demand')
    fieldset=[('Redcord',{'fields':['target_tut', 'target_teach','target_demand',
                                    'read_user', 'is_active']})]





admin.site.register(FB_item_code,FB_item_codeAdmin)
admin.site.register(SearchRecord,SearchRecordAdmin)
admin.site.register(Read_cnt,ReadCntAdimn)