from django.contrib import admin


from app_board_v2d1.models import \
    Bestclass
# Register your models here.


class BestClassAdmin(admin.ModelAdmin):

    list_display=('id','best_classcard', 'keyword')
    fieldsets=[('best',{'fields':['best_classcard', 'keyword', 'is_active']})]

admin.site.register(Bestclass, BestClassAdmin)