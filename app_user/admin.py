from django.contrib import admin
from app_user.models import UserAccount
# Register your models here.



class UserAccountAdmin(admin.ModelAdmin):
    search_fields = ['email', 'firstname', 'lastname']
    list_display = ('email', 'firstname', 'lastname', 'created_at')

    fieldsets = [("AccountInfo",{'fields':['djgouser', 'email', 'firstname', 'lastname', 'propic']})]


admin.site.register(UserAccount, UserAccountAdmin)