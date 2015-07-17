from django.contrib import admin
from app_user.models import UserProfile
# Register your models here.



class ProfileAdmin(admin.ModelAdmin):
    list_display = ('djgouser', 'created_at')

    fieldsets = [("AccountInfo",{'fields':['djgouser', 'propic']})]


admin.site.register(UserProfile, ProfileAdmin)