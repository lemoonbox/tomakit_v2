from django.db import models
from django.conf import settings

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

class ClassInteract(models.Model):
    view_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)
    contact_count = models.IntegerField(default=0)

class ClassPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=150, null=False)
    category = models.ManyToManyField(ClassCategory, null=False)
    price = models.IntegerField(null=True)
    price_tag = models.ManyToManyField(PriceTag)
    day=models.CharField(max_length=70, null=False)
    time=models.CharField(max_length=70, null=False)
    mem_num=models.IntegerField(null=False)
    video_url=models.URLField(null=True, blank=True)

    contact_tel = models.CharField(max_length= 30, null=False)
    address = models.CharField(max_length= 200, null=False)


    postinteract = models.OneToOneField(ClassInteract, null=True)
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

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return  u'%s %s' % (self.post.title, self.post_photo)

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
        return  u'%s %s' % (self.post.title, self.reviewer_name)






