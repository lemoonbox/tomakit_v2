from django.shortcuts import render

from DIY_tool import template_match as TEMP
import \
    string, \
    random


from app_class_v2d1.models import \
    T2TeachClass, \
    T2TutClass

from app_payment_v2d1.forms import \
    PayPrefillForm
# Create your views here.


def pay_prefill(request):

    if request.method == "GET":
        post_id=request.GET.get("post_id", "")
        _classtype=request.GET.get('classtype', "")
        key=""
        for i in xrange(8):
            key = key+random.choice(string.ascii_letters\
                +string.digits)

        merchant_id="merchant_id_cid_"+post_id+"_"+key

        if _classtype == "tutclass":
            _post=T2TutClass.objects.get(pk=post_id)
        else:
            _post=T2TeachClass.objects.get(pk=post_id)
    else :
        pass

    return render(request, TEMP.PRE_PAYMENT_V2D1,{
        "post":_post,
        "merchant_id":merchant_id,
    })


def pay_conf(request):

    if request.method == "GET":
        _post=""
        post_id=request.GET.get("post_id", "")
        _classtype=request.GET.get('classtype', "")
        mobli1=request.GET.get("mobli2", "")
        mobli1=request.GET.get("mobli3", "")
        merchant_id=request.GET.get("merchant_id", "")
        prefillform=PayPrefillForm(request.GET)

        if prefillform.is_valid():
            pass
        else:
            if _classtype == "tutclass":
                _post=T2TutClass.objects.get(pk=post_id)
            else:
                _post=T2TeachClass.objects.get(pk=post_id)
            return render(request,TEMP.PAYMENT_CONF_V2D1,{
                    'post':_post,
                    "merchant_id":merchant_id,
                })

    return render(request,TEMP.PRE_PAYMENT_V2D1,{
        "prefillform":prefillform,
        'post':_post,
        "merchant_id":merchant_id,
    })
