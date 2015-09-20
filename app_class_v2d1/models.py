from django.db import models

from django.conf import settings
from app_comminfo.models import \
    Category, \
    State
import uuid

# Create your models here.
def upload_to(instance, filename):
    path_arr = filename.split('.')
    return 'lessonimage/%s' %( str(uuid.uuid4())+"."+path_arr[-1])

def review_upload_to(instance, filename):
    path_arr = filename.split('.')
    return 'lessonimage/review/%s' %( str(uuid.uuid4())+"."+path_arr[-1])

class T2TeachClass(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL)
    category=models.ForeignKey(Category)
    classtype=models.CharField(max_length=100)
    title=models.CharField(max_length=150)
    intro_line=models.CharField(max_length=250)
    repeat=models.IntegerField(null=True, blank=True)
    perhour=models.IntegerField(null=True, blank=True)
    weekday=models.CharField(max_length=150,null=True, blank=True)
    max_num=models.IntegerField(null=True, blank=True)
    min_num=models.IntegerField(null=True, blank=True)
    startday=models.DateField(null=True, blank=True)
    deadline=models.DateField(null=True, blank=True)
    price=models.IntegerField(null=True, blank=True)
    extra_price=models.IntegerField(null=True, blank=True)
    video=models.CharField(max_length=100,null=True, blank=True)
    descript=models.TextField(null=True, blank=True)
    curri=models.TextField(null=True, blank=True)
    notic=models.TextField(null=True, blank=True)
    state=models.ForeignKey(State,null=True, blank=True)
    addr=models.CharField(max_length=100,null=True, blank=True)
    addr_detail=models.CharField(max_length=100,null=True, blank=True)

    wr_done=models.BooleanField(default=False)
    deadline_over=models.BooleanField(default=False)
    is_open=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

    def __unicode__(self):
        return  u'%s %s' % (self.id, self.title)

class T2TutClass(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL)
    category=models.ForeignKey(Category)
    classtype=models.CharField(max_length=100)
    title=models.CharField(max_length=150)
    intro_line=models.CharField(max_length=250)
    repeat=models.IntegerField(null=True, blank=True)
    perhour=models.IntegerField(null=True, blank=True)
    weekday=models.CharField(max_length=150,null=True, blank=True)
    price=models.IntegerField(null=True, blank=True)
    extra_price=models.IntegerField(null=True, blank=True)
    video=models.CharField(max_length=100,null=True, blank=True)
    descript=models.TextField(null=True, blank=True)
    curri=models.TextField(null=True, blank=True)
    notic=models.TextField(null=True, blank=True)
    state=models.ForeignKey(State,null=True, blank=True)
    addr=models.CharField(max_length=100,null=True, blank=True)
    addr_detail=models.CharField(max_length=100,null=True, blank=True)

    wr_done=models.BooleanField(default=False)
    deadline_over=models.BooleanField(default=False)
    is_open=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

    def __unicode__(self):
        return  u'%s %s' % (self.id, self.title)

class T2ClassCard(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL)
    category=models.ForeignKey(Category)
    state=models.ForeignKey(State)
    teach_post=models.ForeignKey(T2TeachClass, null=True, blank=True)
    tut_post=models.ForeignKey(T2TutClass, null=True, blank=True)
    classtype=models.CharField(max_length=100)
    class_id=models.IntegerField()
    title=models.CharField(max_length=100)
    intro_line=models.CharField(max_length=100)
    repeat=models.IntegerField()
    perhour=models.IntegerField()
    price=models.IntegerField()
    extra_price=models.IntegerField()

    wr_done=models.BooleanField(default=False)
    deadline_over=models.BooleanField(default=False)
    is_open=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)

    pop_point=models.IntegerField(default=100000)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    def __unicode__(self):
        return  u'%s %s' % (self.id, self.title)


class T2ClassPic(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL)
    teach_post=models.ForeignKey(T2TeachClass, null=True, blank=True)
    tut_post=models.ForeignKey(T2TutClass, null=True, blank=True)
    class_card=models.ForeignKey(T2ClassCard)
    image = models.ImageField(null=True, upload_to=upload_to)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return  u'%s %s' % (self.id, self.image)

class T2ClassReview(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, related_name="my_review")
    host_user=models.ForeignKey(settings.AUTH_USER_MODEL, related_name="host_review")
    teach_post=models.ForeignKey(T2TeachClass, null=True, blank=True)
    tut_post=models.ForeignKey(T2TutClass, null=True, blank=True)
    grade=models.IntegerField()
    review=models.TextField()
    image = models.ImageField(null=True, upload_to=review_upload_to)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return  u'%s %s' % (self.id, self.review)

