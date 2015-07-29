from django.contrib import admin
from app_question.models import QItem, QPic, QSkill
# Register your models here.


class QItemAdmin(admin.ModelAdmin):
    list_filter = ['title', 'djgouser', 'mylocal',]

    list_display = ('title', 'mylocal', 'memnum')

    fieldsets = [("QItem", {'fields':['djgouser', 'category','title', 'state','mylocal', 'wantedu',
                                      'memnum', 'mobile',]}),]
admin.site.register(QItem, QItemAdmin)

class QPicAdmin(admin.ModelAdmin):
    list_filter = ['user', 'qitem',]

    list_display = ('created_at', 'qitem', id)

    fieldsets = [("QPic", {'fields':['user', 'qitem', 'category','pic',]}),]

admin.site.register(QPic, QPicAdmin)

class QSkillAdmin(admin.ModelAdmin):
    list_filter = ['title', 'djgouser', 'mylocal',]

    list_display = ('title', 'mylocal', 'memnum')

    fieldsets = [("QItem", {'fields':['djgouser', 'category','title', 'state','mylocal',
                                      'wantgoal','wantclass','wantedu',
                                      'memnum', 'mobile',]}),]
admin.site.register(QSkill, QSkillAdmin)