#coding: utf-8
from django.db import models
from django.conf import settings
# Create your models here.
def upload_to(instance, filename):
    path_arr = filename.split('/')
    return '%s/profile/%s' %(instance.email,path_arr[-1])

class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    nick_name = models.CharField(max_length=20, null=False, blank=False)
    pro_photo = models.ImageField(upload_to=upload_to)
    mobile = models.CharField(max_length=30, unique=True, null=True)
    address = models.CharField(max_length=255, null=True)
    email_confirm = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

class SellerInfo(models.Model):
    user=models.ForeignKey(Profile)
    intro=models.CharField(max_length=150)
    special=models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)



class SignupConfirmKey(models.Model):
    key = models.CharField(max_length=64, null=False, unique=True)
    user = models.ForeignKey(Profile)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)


    @staticmethod
    def find(key):
        ret = SignupConfirmKey.objects.filter(key=key)
        if (not ret.exists()): return None

        return  ret


class PasswordResetKeys(models.Model):
    key = models.CharField(max_length=64, null=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    @staticmethod
    def find(key):
        ret = PasswordResetKeys.objects.filter(key=key)
        if (not ret.exists()): return None


        import datetime
        from django.utils.timezone import utc
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        timeoff = now - ret[0].created_at

        if timeoff.total_seconds()>60*5:
            ret[0].delete()

        return ret[0]

