from django.db import models
from django.conf import settings
import datetime
# Create your models here.


class PrePayment(models.Model):

    user= models.ForeignKey(settings.AUTH_USER_MODEL)
    classtype=models.CharField(max_length=50)
    merchant_uid=models.CharField(max_length=100)
    pay_method=models.CharField(max_length=50)
    amount=models.IntegerField()
    pay_name=models.CharField(max_length=150)
    buyer_name=models.CharField(max_length=50)
    buyer_email=models.CharField(max_length=100)
    buyer_mobli=models.CharField(max_length=100)
    want_day=models.DateField(null=False, default=datetime.date.today())
    want_time=models.CharField(max_length=100, default="default")

    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True, auto_now=False, default=datetime.datetime.now())
    updated_at=models.DateTimeField(auto_now_add=True, auto_now=True, default=datetime.datetime.now())

    def __unicode__(self):
        return  u'%s %s' % (self.id, self.merchant_uid)