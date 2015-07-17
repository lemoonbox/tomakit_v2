from django.db import models
from django.conf import settings

def upload_to(instance, filename):
    path_arr = filename.split('/')
    return '%s/profile/%s' %(instance.djgouser.username, path_arr[-1])



class UserProfile(models.Model):
    djgouser = models.ForeignKey(settings.AUTH_USER_MODEL)
    propic= models.ImageField(upload_to=upload_to)

    mailcnfirm= models.BooleanField(default=False)
    is_activate=models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

    def __unicode__(self):
        return "%s" %(self.djgouser)

class SignupConfirmKey(models.Model):
    key = models.CharField(max_length=64, null=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    created_at = models.DateField(auto_now_add=True, auto_now=False)

    @staticmethod
    def find(key):
        ret = SignupConfirmKey.objects.filter(key=key)
        if (not ret.exists()): return None

        return ret