#coding: utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import \
    login_required
from DIY_tool import template_match as TEMP
import \
    string, \
    random
import datetime
from django.http import\
    HttpResponse,\
    Http404,\
    HttpResponseRedirect

from app_user_v2d1.models import \
    T2Profile
from app_class_v2d1.models import \
    T2TeachClass, \
    T2TutClass

from app_payment_v2d1.forms import \
    PayPrefillForm
from app_payment_v2d1.models import \
    PrePayment
# Create your views here.

@login_required
def pay_prefill(request):
    classtype=""
    if request.method == "GET":
        post_id=request.GET.get("post_id", "")
        classtype=request.GET.get('classtype', "")
        key=""
        for i in xrange(8):
            key = key+random.choice(string.ascii_letters\
                +string.digits)

        merchant_id="merchant_id_cid_"+post_id+"_"+key

        if classtype == "tutclass":
            _post=T2TutClass.objects.get(pk=post_id)
        else:
            _post=T2TeachClass.objects.get(pk=post_id)
    else :
        return Http404("잘못된 요청입니다.")

    return render(request, TEMP.PRE_PAYMENT_V2D1,{
        "post":_post,
        "merchant_id":merchant_id,
        "classtype":classtype
    })

@login_required
def pay_conf(request):
    if request.method == "POST":
        HTTP_HOST=request.META["HTTP_HOST"]
        _post=""
        post_id=request.POST.get("post_id", "")
        classtype=request.POST.get('classtype', "")
        mobli2=request.POST.get("mobli2", "")
        mobli3=request.POST.get("mobli3", "")
        mobli=mobli2+mobli3
        merchant_id=request.POST.get("merchant_id", "")
        buyer_name=request.POST.get('buyer_name', "")
        buyer_email=request.POST.get('buyer_email', "")
        pay_method=request.POST.get('pay_method', "")
        prefillform=PayPrefillForm(request.POST)
        want_day=request.POST.get("want_day", "")

        _profile=T2Profile.objects.get(user=request.user)
        _profile.mobli=mobli
        _profile.mobli_able=True
        _profile.save()
        vbank_due= datetime.date.today()+datetime.timedelta(days=1)
        if classtype == "tutclass":
            _post=T2TutClass.objects.get(pk=post_id)
        else:
            _post=T2TeachClass.objects.get(pk=post_id)
        if prefillform.is_valid():
            _prepayment=PrePayment(user=request.user, classtype=classtype,
                                   merchant_uid=merchant_id, pay_method=pay_method,
                                   amount=_post.price+_post.extra_price,
                                   pay_name=_post.title, buyer_name=buyer_name,
                                   buyer_email=buyer_email, buyer_mobli=mobli,
                                   want_day=want_day)
            _prepayment.save()
            return render(request,TEMP.PAYMENT_CONF_V2D1,{
                    "prefillform":prefillform,
                    'post':_post,
                    "merchant_id":merchant_id,
                    'buyer_name':buyer_name,
                    'mobli':mobli,
                    'buyer_email':buyer_email,
                    "classtype":classtype,
                    "want_day":want_day,
                    "pay_method":pay_method,
                    "vbank_due":vbank_due,
                    "amount":str(_post.price+_post.extra_price),
                    "HTTP_HOST":HTTP_HOST,
                })
    return render(request,TEMP.PRE_PAYMENT_V2D1,{
        "prefillform":prefillform,
        'post':_post,
        "merchant_id":merchant_id,
        'buyer_name':buyer_name,
        'mobli':mobli,
        'buyer_email':buyer_email,
        'classtype':classtype,
    })

@login_required
def payment_finish(request):

    if request.method == "GET":
        rsp=request.GET.get("rsp", "")
        if rsp=="success":
            return render(request, TEMP.PAYMENT_FINSIH_V2D1, {})
        else:
            return render(request, TEMP.PAYMENT_FAIL_V2D1, {
            })
    else:
        return Http404("잘못된 요청입니다.")