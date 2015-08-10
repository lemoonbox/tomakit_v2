from django.contrib import admin
from app_board.models import \
    Questionbox,\
    SolutionBox, \
    Casebox, \
    MainQoubox
# Register your models here.


##inline classes#####
class CaseBoxInline(admin.TabularInline):

    fieldsets =(('casebox',
                 {'fields':('qtype', 'category', 'state',
                            'quebox', 'solubox',)}
                ),)
    model = Casebox

    def get_max_num(self, request, obj=None, **kwargs):
        max_num =1

        return max_num
    extra = 0

class QueBoxInline(admin.StackedInline):

    fieldsets =(('solubox_is_solved',
                 {'fields':('is_solved',)}
                ),)
    model = Questionbox

    def get_max_num(self, request, obj=None, **kwargs):
        max_num =1

        return max_num
    extra = 0

class QusetionBoxAdmin(admin.ModelAdmin):
    list_filter = ['title', 'djgouser', 'mylocal',]

    list_display = ('title', 'qtype','mylocal',)

    fieldsets = [("Qbox", {'fields':['djgouser', 'category','title',
                                     'weekday', 'state','mylocal',
                                     'qtype','qitempost','qskillpost',
                                      'skill_class', 'skill_goal', 'skill_edu',
                                     'item_pic','is_solved']}),]
admin.site.register(Questionbox, QusetionBoxAdmin)

class SolutionBoxAdmin(admin.ModelAdmin):
    list_filter = ['title', 'djgouser', 'mylocal',]

    list_display = ('title', 'qtype','mylocal','price')

    fieldsets = [("Solubox", {'fields':['djgouser','title', 'qtype',
                                      'qitempost','qskillpost',
                                      'state','mylocal', 'repeat',
                                      'perhour', 'weekday_time', 'price']}),]
    inlines = (CaseBoxInline,)

admin.site.register(SolutionBox, SolutionBoxAdmin)


class CaseBoxAdmin(admin.ModelAdmin):
    #list_filter = ['title', 'djgouser', 'mylocal',]

    list_display = ('qtype', 'quebox','solubox')

    fieldsets = [("Casebox", {'fields':['qtype','category', 'state',
                                      'quebox','solubox','is_active',]}),]

admin.site.register(Casebox, CaseBoxAdmin)

class MainboxAdmin(admin.ModelAdmin):

    list_display = ('quebox', 'updated_at')

    fieldsets = [("MainQoubox", {'fields':['quebox','is_active',]}),]

admin.site.register(MainQoubox, MainboxAdmin)