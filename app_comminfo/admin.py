from django.contrib import admin
from app_comminfo.models import State, Category
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)
    fieldsets = [('Cate',{'fields':['category', 'is_active',]},)]


admin.site.register(Category, CategoryAdmin)


class StateAdmin(admin.ModelAdmin):
    list_display = ('state',)
    fieldsets = [('Cate',{'fields':['state', 'is_active',]},)]


admin.site.register(State, StateAdmin)