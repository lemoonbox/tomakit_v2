from django.db import models
from django.conf import settings

from django_summernote import models as summer_model
from django_summernote import fields as summer_fields
# Create your models here.

def upload_to(instance, filename):
    return 'classpic/%s/%s' %(instance.classpost.id,filename)

def review_upload_to(instance, filename):
    return 'classpic/%s/review/%s' %(instance.classpost.id,filename)

class ClassCategory(models.Model):
    category_name = models.CharField(max_length=100, null=False)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_active = models.BooleanField(default=True)


    def __unicode__(self):
        return u'%s' % (self.category_name)

class PriceTag(models.Model):
    price_tag = models.CharField(max_length=100, null=False)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % (self.price_tag)


class ClassInteract(models.Model):
    view_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)
    buy_count = models.IntegerField(default=0)

    def __unicode__(self):
        return u'view: %s, shar: %s, buy:%s' %(self.view_count, self.share_count, self.buy_count)

class ClassPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    seo_title=models.CharField(max_length=150, null=False)
    title = models.CharField(max_length=150, null=False)
    category = models.ManyToManyField(ClassCategory, null=False)
    price = models.IntegerField(null=True)
    price_tag = models.ManyToManyField(PriceTag)
    day=models.CharField(max_length=70, null=False)
    time=models.CharField(max_length=70, null=False)
    mem_num=models.IntegerField(null=False)

    video_url=models.CharField(max_length=150, blank=True)
    need1=models.CharField(max_length=50, null=False)
    need1_detail=models.CharField(max_length=150, null=False)
    need2=models.CharField(max_length=50, null=False)
    need2_detail=models.CharField(max_length=150, null=False)

    contact_tel = models.CharField(max_length= 30, null=False)
    address = models.CharField(max_length= 200, null=False)


    postinteract=models.OneToOneField(ClassInteract, null=True, related_name='class_post')
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % (self.title)


class ClassPic(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    classpost = models.ForeignKey(ClassPost)
    category = models.ManyToManyField(ClassCategory, null=False)
    class_photo = models.ImageField(null=True, upload_to=upload_to)
    photo_title = models.CharField(max_length=100, null=False)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return  u'%s %s' % (self.classpost.title, self.class_photo)

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    classpost = models.ForeignKey(ClassPost)
    category = models.ManyToManyField(ClassCategory, null=False)
    review=models.CharField(max_length=150, null=False)
    reviewer_photo=models.ImageField(null=True, upload_to=review_upload_to)
    reviewer_name=models.CharField(max_length=100, null=False)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return  u'%s' % (self.reviewer_name)


class ClassCurri(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    classpost = models.ForeignKey(ClassPost)
    category = models.ManyToManyField(ClassCategory, null=False)
    curri_name=models.CharField(max_length=100, null=False)
    curri_detail=models.TextField(null=False)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return  u'%s' % (self.curri_name)

#####summer
class ClassDetail(summer_model.Attachment):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(ClassPost)
    category = models.ManyToManyField(ClassCategory)
    class_detail = summer_fields.SummernoteTextField()

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return  u'%s %s' % (self.user, self.class_detail)

class CostInfo(models.Model):
    classpost = models.OneToOneField(ClassPost)
    apply_url= models.CharField(max_length=150, null=True)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

    def __unicode__(self):
        return u'%s %s' %(self.classpost, self.apply_url)



