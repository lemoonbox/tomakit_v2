from django.contrib import admin
from app_payment_v2d1.models import PrePayment
# Register your models here.
class PrePaymentAdmin(admin.ModelAdmin):

    list_display=('user','merchant_uid', 'pay_method','created_at','updated_at')
    fieldsets=[("payInfo",{'fields':['user','classtype', 'merchant_uid',
                                        'pay_method','amount', 'pay_name',
                                        'buyer_name', 'buyer_email','buyer_mobli',
                                        'want_day']})]

admin.site.register(PrePayment, PrePaymentAdmin)