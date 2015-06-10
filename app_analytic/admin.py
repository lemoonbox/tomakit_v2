from django.contrib import admin
from app_analytic.models import FB_item_code
# Register your models here.

class FB_item_codeAdmin(admin.ModelAdmin):

    search_fields = ['classpost',]

    list_display = ('classpost',)
    fieldsets = [('Post',{'fields':['buy_C','read_C', 'retarget_C', 'classpost']}),
                 ('postinfo',{'fields':['is_active',]})]


admin.site.register(FB_item_code,FB_item_codeAdmin)