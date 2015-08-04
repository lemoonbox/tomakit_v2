#coding: utf-8
from django.db import models
from django.conf import settings
from datetime import datetime

from app_comminfo.models import State, Category
from app_question.models import QPic, QSkill, QItem
import uuid

# Create your models here.

class Questionbox(models.Model):

    Q_TYPE_CHOICES =(
        ("S", 'Skill'),
        ("I", 'Item'),
    )
    #model.get_F00_display()

    djgouser = models.ForeignKey(settings.AUTH_USER_MODEL)
    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=150, null=False)
    weekday = models.CharField(max_length=150, null=False, default=u"날짜협의")
    state = models.ManyToManyField(State)
    mylocal = models.CharField(max_length=150, null=False)
    qtype = models.CharField(max_length=1,
                             choices=Q_TYPE_CHOICES,)
    qitempost = models.OneToOneField(QItem, null=True, blank=True)
    qskillpost = models.OneToOneField(QSkill, null=True, blank=True)
    skill_class = models.TextField(null=True, blank=True)
    skill_goal = models.TextField(null=True, blank=True)
    skill_edu = models.TextField(null=True, blank=True)
    item_pic = models.ImageField(QPic,blank=True)

    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    is_active = models.BooleanField(default=True)
    is_solved = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s::%s::%s" %(self.qtype, self.title, self.id)

class SolutionBox(models.Model):

    Q_TYPE_CHOICES =(
        ("S", 'Skill'),
        ("I", 'Item'),
    )
    djgouser = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=150, null=False)
    qtype = models.CharField(max_length=1,
                             choices=Q_TYPE_CHOICES,)
    qoubox = models.ForeignKey(Questionbox, null=True)
    qitempost = models.ForeignKey(QItem, null=True, blank=True, related_name='solustionbox')
    qskillpost = models.ForeignKey(QSkill, null=True, blank=True, related_name='solustionbox')
    state = models.ManyToManyField(State)
    mylocal = models.CharField(max_length=150, null=False)
    repeat = models.IntegerField(default=1, null=True, blank=True)
    perhour = models.IntegerField(default=0, null=True, blank=True)
    weekday_time = models.CharField(max_length=100, null=False)
    price = models.IntegerField(default=1, null=False)

    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s::%s::%s" %(self.qtype, self.title, self.id)



class Casebox(models.Model):
    Q_TYPE_CHOICES =(
        ("S", 'Skill'),
        ("I", 'Item'),
    )
    qtype = models.CharField(max_length=1,
                             choices=Q_TYPE_CHOICES,)
    category = models.ManyToManyField(Category)
    state = models.ManyToManyField(State)
    quebox= models.ForeignKey(Questionbox, null=False, related_name='Casebox')
    solubox = models.ForeignKey(SolutionBox, null=False, related_name='Casebox')

    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s::%s" %(self.quebox.title, self.solubox.title)


class MainQoubox(models.Model):

    quebox= models.ForeignKey(Questionbox, null=False, related_name='Mainbox')
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s" %(self.quebox.title,)