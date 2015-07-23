from django.db import models
from django.conf import settings

# Create your models here.

class QItem(models.Model):
    djgouser = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField()