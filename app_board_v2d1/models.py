from django.db import models

from app_class_v2d1.models import \
    T2ClassCard

# Create your models here.


class Bestclass(models.Model):
    best_classcard=models.OneToOneField(T2ClassCard)
    keyword=models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return  u'%s:: %s::%s' % (self.id, self.best_classcard, self.keyword)
