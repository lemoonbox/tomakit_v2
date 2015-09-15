#coding: utf-8
from django.db import models
from django.conf import settings
import uuid

def upload_to(instance, filename):
    path_arr = filename.split('.')
    return 'profile/%s/%s' %(instance.user.username, str(uuid.uuid4())+"."+path_arr[-1])

def potpolio_upload_to(instance, filename):
    path_arr = filename.split('.')
    return 'potpolio/%s/%s' %(instance.user.username, str(uuid.uuid4())+"."+path_arr[-1])

class T2Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    mail_conf=models.BooleanField(default=False)
    pro_pic=models.ImageField(upload_to=upload_to, null=True, blank=True)
    intro_line=models.CharField(max_length=250, null=True, blank=True)
    mobli1=models.CharField(max_length=50, null=True, blank=True)
    mobli2=models.CharField(max_length=50, null=True, blank=True)
    mobli=models.CharField(max_length=50, null=True, blank=True)
    mobli_able=models.BooleanField(default=False)
    mobli_conf=models.BooleanField(default=False)
    is_host=models.BooleanField(default=False)

    is_activate=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at=models.DateTimeField(auto_now_add=True, auto_now=True)

    @staticmethod
    def mobli_on(user, mobile1, mobile2):
        _profile=T2Profile.objects.get(user=user)
        _profile.mobli1=mobile1
        _profile.mobli2=mobile2
        _profile.mobli=mobile1+mobile2
        _profile.mobli_able=True
        _profile.save()



class T2SignupConfirmKey(models.Model):
    key=models.CharField(max_length=64, null=False, unique=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL)

    created_at=models.DateField(auto_now_add=True, auto_now=False)

    @staticmethod
    def find(key):
        ret=T2SignupConfirmKey.objects.filter(key=key)
        if (not ret.exists()): return None

        return ret


class T2PWResetKeys(models.Model):
    key=models.CharField(max_length=64, null=False, unique=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL)

    created_at=models.DateTimeField(auto_now_add=True, auto_now=False)


    @staticmethod
    def find(key):
        ret=T2PWResetKeys.objects.filter(key=key)
        if not ret.exists(): return None

        import datetime
        from django.utils.timezone import utc
        now=datetime.datetime.utcnow().replace(tzinfo=utc)
        timeoff=now - ret[0].created_at

        if timeoff.total_seconds()>60*5:
            ret[0].delete()
            return None

        return ret[0]

class T2HostProfile(models.Model):

    TYPE_CHOICES = (
        (u'work', 'workshop'),
        (u'tutor', 'tutor')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    intro_video=models.CharField(max_length=100, null=True, blank=True)
    intro_pic=models.ImageField(upload_to=upload_to, null=True, blank=True)
    intro_self=models.TextField(null=True, blank=True)
    shop_addr=models.CharField(max_length=250, null=True, blank=True)
    shop_addr_detail=models.CharField(max_length=250, null=True, blank=True)
    hosttype= models.CharField(max_length=50, null=False, unique=False,
                               choices=TYPE_CHOICES)

    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at=models.DateTimeField(auto_now_add=True, auto_now=True)

class T2HostApply(models.Model):

    user=models.ForeignKey(settings.AUTH_USER_MODEL)
    introduce=models.TextField()
    mobli=models.CharField(max_length=100)
    hosttype=models.CharField(max_length=100)
    local=models.CharField(max_length=150)
    site=models.CharField(max_length=250, null=True, blank=True,)
    potpolio=models.FileField(null=True, blank=True,upload_to=potpolio_upload_to)

    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at=models.DateTimeField(auto_now_add=True, auto_now=True)
