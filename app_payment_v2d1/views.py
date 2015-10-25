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
    HTTP_HOST=request.META["HTTP_HOST"]
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
            merchant_id+=_post.title
        else:
            _post=T2TeachClass.objects.get(pk=post_id)
            merchant_id+=_post.title
    else :
        return Http404("잘못된 요청입니다.")

    return render(request, TEMP.PRE_PAYMENT_V2D1,{
        "post":_post,
        "merchant_id":merchant_id,
        "classtype":classtype,
        "HTTP_HOST":HTTP_HOST,
    })

@login_required
def pay_conf(request):
    HTTP_HOST=request.META["HTTP_HOST"]
    if request.method == "POST":
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
        want_time=request.POST.get("want_time", "")
        vbank_due= datetime.date.today()+datetime.timedelta(days=1)


        if classtype == "tutclass":
            if want_day :
                want_day=datetime.datetime.strptime(
                    want_day, '%Y/%m/%d').strftime("%Y-%m-%d")
            _post=T2TutClass.objects.get(pk=post_id)
        elif classtype == "teachclass":
            want_day=datetime.date.today()
            _post=T2TeachClass.objects.get(pk=post_id)

        if prefillform.is_valid() and want_day and len(mobli)<40:
            _profile=T2Profile.objects.get(user=request.user)
            _profile.mobli1=mobli2
            _profile.mobli2=mobli3
            _profile.mobli=mobli
            _profile.mobli_able=True
            _profile.save()
            _prepayment=PrePayment(user=request.user, classtype=classtype,
                                   merchant_uid=merchant_id, pay_method=pay_method,
                                   amount=_post.price+_post.extra_price,
                                   pay_name=_post.title, buyer_name=buyer_name,
                                   buyer_email=buyer_email, buyer_mobli=mobli,
                                   want_day=want_day, want_time=want_time)
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
        else:
            if len(mobli)>40:
                prefillform.add_error("mobli2", u"정상적인 전화번호를 입력해주세요")
            else:
                prefillform.add_error("want_day", u"희망 날짜를 선택해주세요")
    return render(request,TEMP.PRE_PAYMENT_V2D1,{
        "prefillform":prefillform,
        'post':_post,
        "merchant_id":merchant_id,
        'buyer_name':buyer_name,
        'mobli':mobli,
        'buyer_email':buyer_email,
        'classtype':classtype,
        "HTTP_HOST":HTTP_HOST,
    })

@login_required
def payment_finish(request):
    HTTP_HOST=request.META["HTTP_HOST"]
    if request.method == "GET":
        rsp=request.GET.get("rsp", "")
        if rsp=="success":
            return render(request, TEMP.PAYMENT_FINSIH_V2D1, {
                "HTTP_HOST":HTTP_HOST,
            })
        else:
            return render(request, TEMP.PAYMENT_FAIL_V2D1, {
                 "HTTP_HOST":HTTP_HOST,
            })
    else:
        return Http404("잘못된 요청입니다.")