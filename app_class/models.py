#coding: utf-8
from django.db import \
    models
from django.conf import \
    settings
# Create your models here.

def upload_to(instance, filename):
    print instance.class_post.id
    path_arr = filename.split('/')
    return 'class_pic/%s/%s' %(instance.class_post.id,path_arr[-1])

class ClassPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=150, null=False)
    price = models.IntegerField(null=False)
    describe = models.TextField(max_length=500, null=False)

    #it is can't user form
    lessonday = models.DateField(null=False)
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=False)
    ####
    minimum = models.IntegerField(null=False)
    maximum = models.IntegerField(null=False)

    contact_tel = models.CharField(max_length= 30, null=False)
    address = models.CharField(max_length= 200, null=False)
    #latitude = models.DecimalField(max_digits =7, decimal_places=6)
    #longitude = models.DecimalField(max_digits=7, decimal_places=6)
    #content = models.TextField(null=False)


    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_active = models.BooleanField(default=True)


class ClassPic(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    class_post = models.ForeignKey(ClassPost)
    class_photo = models.ImageField(null=True, upload_to=upload_to)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_active = models.BooleanField(default=True)

