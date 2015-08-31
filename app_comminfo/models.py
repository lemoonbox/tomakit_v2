from django.db import models
import uuid

# Create your models here.
def upload_to(instance, filenmae):
    #folder_name = instance.qitem.title + instance.qitem.id
    nmparts=filenmae.split(".")
    print nmparts
    return 'comminfo/catepic/%s' %(str(uuid.uuid4())+"."+nmparts[-1])

class Category(models.Model):
    category = models.CharField(max_length=100, null=False)
    cate_pic = models.ImageField(null=True, upload_to=upload_to)

    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s' %(self.category)


class State(models.Model):
    state = models.CharField(max_length=100, null=False)

    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s' %(self.state)
