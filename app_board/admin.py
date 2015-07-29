from django.contrib import admin
from app_board.models import Questionbox, SolutionBox, Casebox
# Register your models here.


class QusetionBoxAdmin(admin.ModelAdmin):
    list_filter = ['title', 'djgouser', 'mylocal',]

    list_display = ('title', 'qtype','mylocal',)

    fieldsets = [("Qbox", {'fields':['djgouser', 'category','title',
                                     'weekday', 'state','mylocal',
                                     'qtype','qitempost','qskillpost',
                                      'skill_class', 'skill_goal', 'skill_edu',
                                     'item_pic',]}),]
admin.site.register(Questionbox, QusetionBoxAdmin)

class SolutionBoxAdmin(admin.ModelAdmin):
    list_filter = ['title', 'djgouser', 'mylocal',]

    list_display = ('title', 'qtype','mylocal','price')

    fieldsets = [("Solubox", {'fields':['djgouser','title', 'qtype',
                                      'qitempost','qskillpost',
                                      'state','mylocal', 'repeat',
                                      'perhour', 'weekday_time', 'price']}),]
admin.site.register(SolutionBox, SolutionBoxAdmin)


class CaseBoxAdmin(admin.ModelAdmin):
    #list_filter = ['title', 'djgouser', 'mylocal',]

    list_display = ('qtype', 'quebox','solubox')

    fieldsets = [("Casebox", {'fields':['qtype','category', 'state',
                                      'quebox','solubox','is_active',]}),]
admin.site.register(Casebox, CaseBoxAdmin)