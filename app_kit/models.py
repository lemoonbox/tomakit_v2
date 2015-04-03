#coding: utf-8
from django.db import \
    models
from django.conf import \
    settings
from django_summernote import models as summer_model
from django_summernote import fields as summer_fields
import uuid
import os
from datetime import datetime

# Create your models here.

def upload_to(instance, filename):
    return 'kit_pic/%s/%s' %(instance.kit_post.id,filename)


class Kit_Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    category = models.CharField(null=False, max_length=120)
    title = models.CharField(max_length=150, null=False)
    price = models.IntegerField(null=False)
    describe = models.TextField(max_length=500, null=False)

    contact_tel = models.CharField(max_length= 30, null=False)
    address = models.CharField(max_length= 200, null=False)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_active = models.BooleanField(default=True)


class Kit_Photo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    kit_post = models.ForeignKey(Kit_Post)
    kit_photo = models.ImageField(null=True, upload_to=upload_to)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_active = models.BooleanField(default=True)



class Kit_Detail(summer_model.Attachment):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    kit_post = models.ForeignKey(Kit_Post)
    kit_detail = summer_fields.SummernoteTextField()

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_active = models.BooleanField(default=True)
