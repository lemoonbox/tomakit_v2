from django.db import models

# Create your models here.


class Category(models.Model):
    category = models.CharField(max_length=100, null=False)

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
