from django.db import models
from app_class.models import ClassPost
from django.conf import settings


class FB_item_code(models.Model):
    buy_C=models.TextField(null=True, unique=False)
    read_C = models.TextField(null=True, unique=False)
    retarget_C=models.TextField(null=True, unique=False)
    classpost=models.OneToOneField(ClassPost, null=False)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % (self.class_post)