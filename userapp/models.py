#coding: utf-8
from django.db import models
from django.conf import settings
# Create your models here.

def upload_to(instance, filename):
    return '%s/profile/%s' %(instance.email,filename)

class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    pro_photo = models.ImageField(upload_to=upload_to)
    mobile = models.CharField(max_length=30, unique=True)
    address = models.CharField(max_length=255, null=False)
    email_confirm = models.BooleanField(default=False)



    @staticmethod
    def create(_user, email, mobile, address):

        profile = Profile(user=_user, email=email,
                          mobile=mobile, address=address)

        profile.save()


        return profile


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

        if timeoff.total_seconds()>60*20:
            ret[0].delete()

        return ret[0]