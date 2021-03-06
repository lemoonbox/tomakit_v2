from django.db import models
from django.conf import settings
import uuid
import requests
from PIL import Image
from StringIO import StringIO

from app_comminfo.models import State, Category

from datetime import datetime

# Create your models here.


def upload_to(instance, filename):
    nmparts=filename.split(".")
    return "DeamndImage/post%s/%s" %(instance.demand_post.id, str(uuid.uuid4())+"."+nmparts[-1])

class T2ClassDemand(models.Model):

    user=models.ForeignKey(settings.AUTH_USER_MODEL)
    category=models.ForeignKey(Category)
    title=models.CharField(max_length=250, null=True, blank=True)
    descript=models.TextField(null=True, blank=True)
    state=models.ForeignKey(State)
    local=models.CharField(max_length=100, null=True, blank=True)
    weekday=models.CharField(max_length=100, null=True, blank=True)
    goal=models.CharField(max_length=100, null=True, blank=True)
    inline_cnt=models.IntegerField(null=True, blank=True)
    inline_users=models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name="myinline_demand_set",
                                        null=True, blank=True)
    min_price=models.IntegerField(null=True, blank=True)
    max_price=models.IntegerField(null=True, blank=True)

    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at=models.DateTimeField(auto_now_add=True, auto_now=True)

    def __unicode__(self):
        return  u'%s %s' % (self.id, self.title)

class T2DemandCard(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL)
    demand_id=models.IntegerField()
    demand_post=models.OneToOneField(T2ClassDemand)
    category=models.ForeignKey(Category)
    title=models.CharField(max_length=250, null=True, blank=True)
    state=models.ForeignKey(State)
    descript=models.TextField(null=True, blank=True)
    inline_cnt=models.IntegerField(null=True, blank=True)
    inline_users=models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name="myinline_demand_card_set")
    min_price=models.IntegerField()
    max_price=models.IntegerField()

    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at=models.DateTimeField(auto_now_add=True, auto_now=True)

    def __unicode__(self):
        return  u'%s %s' % (self.id, self.title)

class T2DemandPic(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL)
    demand_post=models.ForeignKey(T2ClassDemand)
    demand_card=models.ForeignKey(T2DemandCard)
    image = models.ImageField(null=True, upload_to=upload_to)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return  u'%s %s' % (self.id, self.image)

    @staticmethod
    def base64_imglist(url_set, _demand_post):
        img_arr=[]
        _img_qset=T2DemandPic.objects.filter(demand_post=_demand_post)
        for db_images in _img_qset:
            img_info=[]
            url =url_set+str(db_images.image)
            img_res = requests.get(url)
            img = Image.open(StringIO(img_res.content))
            output = StringIO()
            img.save(output, format="PNG")
            contents = output.getvalue().encode("base64")
            output.close()
            img_info.append(db_images.id)
            img_info.append(db_images.image)
            img_info.append(contents)
            img_arr.append(img_info)
        return img_arr


class T2DemandCmt(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL)
    demand_post=models.ForeignKey(T2ClassDemand)
    comment=models.CharField(max_length=250, null=False, blank=False)
    class_ad=models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return  u'%s %s' % (self.id, self.demand_post)
