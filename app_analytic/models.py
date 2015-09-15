from django.db import models
from django.conf import settings

from app_class_v2d1.models import \
    T2TeachClass, \
    T2TutClass
from app_demand_v2d1.models import \
    T2ClassDemand
from app_comminfo.models import State, Category

class FB_item_code(models.Model):
    buy_C=models.TextField(null=True, unique=False)
    read_C = models.TextField(null=True, unique=False)
    retarget_C=models.TextField(null=True, unique=False)
    tutpost=models.OneToOneField(T2TutClass, null=True)
    teachpost=models.OneToOneField(T2TeachClass, null=True)
    demandpost=models.OneToOneField(T2ClassDemand, null=True)


    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % (self.classpost)

class SearchRecord(models.Model):
    target_cate=models.OneToOneField(State, null=True)
    target_state=models.OneToOneField(Category, null=True)
    target_word=models.CharField(max_length=100, null=True)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s/%s/%s' % (self.target_cate, self.target_state, self.target_word)

class Read_cnt(models.Model):
    target_tut=models.OneToOneField(T2TutClass, null=True)
    target_teach=models.OneToOneField(T2TeachClass, null=True)
    target_demand=models.OneToOneField(T2ClassDemand, null=True)
    read_user=models.ForeignKey(settings.AUTH_USER_MODEL)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return u'read_cnt::%s/%s' % (self.id, self.read_user)
