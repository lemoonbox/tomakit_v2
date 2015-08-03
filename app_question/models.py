from django.db import models
from django.conf import settings
from app_comminfo.models import State, Category
# Create your models here.

def upload_to(instance, filenmae):
    #folder_name = instance.qitem.title + instance.qitem.id
    nmparts=filenmae.split(".")
    print nmparts
    return 'Qitem/%s' %(filenmae)

class QItem(models.Model):
    djgouser = models.ForeignKey(settings.AUTH_USER_MODEL)
    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=150, null=False)
    state = models.ManyToManyField(State)
    mylocal = models.CharField(max_length=150, null=False)
    wantedu = models.TextField()
    memnum = models.IntegerField(default=1)
    mobile = models.CharField(max_length=50, null=False)

    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s::%s" %(self.title, self.id)


class QSkill(models.Model):
    djgouser = models.ForeignKey(settings.AUTH_USER_MODEL)
    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=150, null=False)
    state = models.ManyToManyField(State)
    mylocal = models.CharField(max_length=150, null=False)
    wantclass = models.TextField()
    wantgoal = models.TextField()
    wantedu = models.TextField()
    memnum = models.IntegerField(default=1)
    mobile = models.CharField(max_length=50, null=False)

    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s::%s" %(self.title, self.id)



class QPic(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    qitem = models.ForeignKey(QItem)
    category = models.ManyToManyField(Category)
    pic = models.ImageField(null=True, upload_to=upload_to)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return  u'%s %s' % (self.qitem.title, self.pic)