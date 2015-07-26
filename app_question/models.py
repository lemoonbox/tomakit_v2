from django.db import models
from django.conf import settings

# Create your models here.

class QItem(models.Model):
    djgouser = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=150, null=False)
    mylocal = models.CharField(max_length=150, null=False)
    wantedu = models.TextField()
    memnum = models.IntegerField(default=1)
    mobile = models.CharField(max_length=50, null=False)

    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s" %(self.title)
