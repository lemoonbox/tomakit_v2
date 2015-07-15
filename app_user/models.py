from django.db import models
from django.conf import settings

def upload_to(instance, filename):
    path_arr = filename.split('/')
    return '%s/profile/%s' %(instance.email, path_arr[-1])



class UserAccount(models.Model):
    djgouser = models.ForeignKey(settings.AUTH_USER_MODEL)
    email = models.EmailField(max_length=100, unique=True, blank=False)
    firstname = models.CharField(max_length=20, null=False)
    lastname = models.CharField(max_length=20, null=False)
    propic= models.ImageField(upload_to=upload_to)

    mailcnfirm= models.BooleanField(default=False)
    is_activate=models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

    def __unicode__(self):
        return "%s %s" %(self.lastname, self.firstname)
