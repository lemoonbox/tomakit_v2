from django.db import models
from django.conf import settings

from django_summernote import models as summer_model
from django_summernote import fields as summer_fields
# Create your models here.

def upload_to(instance, filename):
    return '%spic/%s/%s' %(instance.type.type_name, instance.post.id,filename)

class PostType(models.Model):
    type_name = models.CharField(max_length=100, null=False)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_active = models.BooleanField(default=True)


    def __unicode__(self):
        return '%s' % (self.type_name)

class PostCategory(models.Model):
    category_name = models.CharField(max_length=100, null=False)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_active = models.BooleanField(default=True)


    def __unicode__(self):
        return u'%s' % (self.category_name)


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    type = models.ForeignKey(PostType, null=False)
    category = models.ManyToManyField(PostCategory, null=False)
    title = models.CharField(max_length=150, null=False)
    price = models.IntegerField(null=True)
    describe = models.TextField(max_length=500, null=False)


    lessonday = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    ####
    minimum = models.IntegerField(null=True)
    maximum = models.IntegerField(null=True)

    contact_tel = models.CharField(max_length= 30, null=False)
    address = models.CharField(max_length= 200, null=False)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % (self.title)


class PostPic(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    type = models.ForeignKey(PostType)
    category = models.ManyToManyField(PostCategory)
    post_photo = models.ImageField(null=True, upload_to=upload_to)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return  u'%s %s' % (self.post.title, self.post_photo)



class PostDetail(summer_model.Attachment):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    type = models.ForeignKey(PostType)
    category = models.ManyToManyField(PostCategory)
    post_detail = summer_fields.SummernoteTextField()

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return  u'%s %s' % (self.user, self.post_detail)
