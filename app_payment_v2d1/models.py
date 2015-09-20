from django.db import models
from django.conf import settings

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
    want_day=models.DateField(null=False)
