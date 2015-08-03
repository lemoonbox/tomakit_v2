from django.db import models
from django.conf import settings
import uuid

def upload_to(instance, filename):
    path_arr = filename.split('.')
    return 'profile/%s/%s' %(instance.djgouser.username, str(uuid.uuid4())+"."+path_arr[-1])



class UserProfile(models.Model):
    djgouser = models.ForeignKey(settings.AUTH_USER_MODEL)

    propic= models.ImageField(upload_to=upload_to, null=True, blank=True)
    inter_oneline=models.CharField(max_length=150, null=True, blank=True)
    inter_start = models.TextField(null=True, blank=True)
    inter_pic =models.ImageField(upload_to=upload_to, null=True, blank=True)
    inter_url=models.CharField(max_length=150, null=True, blank=True)

    mailcnfirm= models.BooleanField(default=False)
    is_activate=models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

    def __unicode__(self):
        return "%s" %(self.djgouser)

class HostProfile(models.Model):

    TYPE_CHOICES = (
        (u'out', 'outclass'),
        (u'shop', 'shopclass')
    )
    djgouser = models.ForeignKey(settings.AUTH_USER_MODEL)
    mobile = models.CharField(max_length=50, null=False, unique=True)
    hosttype= models.CharField(max_length=50, null=False, unique=True,
                               choices=TYPE_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

class SignupConfirmKey(models.Model):
    key = models.CharField(max_length=64, null=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    created_at = models.DateField(auto_now_add=True, auto_now=False)

    @staticmethod
    def find(key):
        ret = SignupConfirmKey.objects.filter(key=key)
        if (not ret.exists()): return None

        return ret

class PWResetKeys(models.Model):
    key = models.CharField(max_length=64, null=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)


    @staticmethod

    def find(key):
        ret = PWResetKeys.objects.filter(key=key)
        if not ret.exists(): return None

        import datetime
        from django.utils.timezone import utc
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        print type(now)
        print now
        print type(ret[0].created_at)
        print ret[0].created_at
        timeoff = now - ret[0].created_at

        if timeoff.total_seconds()>60*5:
            ret[0].delete()
            return None

        return ret[0]