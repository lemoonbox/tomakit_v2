#coding:utf-8
from django.shortcuts import render
from django.template import \
    Context
from django.shortcuts import \
    render
from django.contrib.auth.models import \
    User
from django.contrib.auth.decorators import \
    login_required
from django.http import \
    HttpResponseRedirect, \
    HttpResponse
import \
    string, \
    random
from django.shortcuts import \
    loader,\
    render
from django.core.context_processors import \
    csrf

from DIY_tool import \
    template_match as TEMP
from DIY_tool.settings import \
    LOCAL as SET_LOCAL
from utils import \
    tasks,\
    utils
from app_user.form import \
    UserForm,\
    PwReset_RequestForm, \
    PwReset_ProcessForm,\
    Send_ConfirmForm, \
    Host_Signup
from app_user.models import \
    UserProfile, \
    SignupConfirmKey, \
    PWResetKeys, \
    HostProfile
# Create your views here.

def signup(request):
    ctx = Context({
        'error':None
    })
    next=""

    if request.method == "GET":
        userForm = UserForm()
        next=request.GET.get("next", "/")
    else:
        userForm = UserForm(request.POST)

        if userForm.is_valid():
            next=request.POST.get("next","/")
            user_data={
                'username': request.POST.get("username", "null"),
                'email':request.POST.get("username", "null"),
                'first_name': request.POST.get('first_name', "null"),
                'last_name': request.POST.get('last_name', "null"),
                'password': request.POST.get('password', "null"),
            }
            if not "null" in user_data.values():
                _user = User.objects.create_user(**user_data)
                _userprofile = UserProfile(djgouser=_user)
                _userprofile.save()

                #send email
                key = utils.generate_key(32,SignupConfirmKey,_user[0])

                host =request.META['HTTP_HOST']
                title = u"안녕하세요! 토마킷입니다. 정식 사용을 승인해주세요."
                sender = "makerecipe@gmail.com"

                if SET_LOCAL:
                   utils.send_key_email(request, title, sender,
                        _user.email, TEMP.V2_CONFIRM_MAIL, key)

                else:
                    tasks.send_key_email.delay(request, title, sender,
                    _user.email, TEMP.V2_PW_RESET_EMAIL, key)

                return HttpResponseRedirect("/v2/user/login/?next="+next)

    return render(request, TEMP.V2_SIGNUP_TEM,{
        'accountform':userForm,
        'next':next,})

@login_required
def host_signup(request):
    ctx = Context({
        'error':None
    })

    _hostprofile = HostProfile.objects.filter(djgouser=request.user)

    if(_hostprofile.exists()):
        tpl = loader.get_template(TEMP.V2_HOST_SIGNUP_REJECT)
        return HttpResponse(tpl.render(ctx))

    if request.method == "GET":
        hostform = Host_Signup()
        next=request.GET.get("next", "/")


    elif request.method=="POST":
        next=request.POST.get("next","/")
        hostform = Host_Signup(request.POST)
        print request.POST["hosttype"]
        print hostform.data

        if hostform.is_valid():
            _hostprofile = HostProfile(djgouser=request.user, mobile=hostform.cleaned_data['mobile'],
                                       hosttype=hostform.cleaned_data['hosttype'])
            _hostprofile.save()

        return HttpResponseRedirect(next)

    return render(request, TEMP.V2_HOST_SIGNUP,{
        'hostform':hostform,
    })



def signup_confirm(request, *args, **kwargs):

    ctx = Context({
        'error':None
    })
    ctx["host"] = request.META['HTTP_HOST']

    _conkey = SignupConfirmKey.find(kwargs['key'])

    if(_conkey):
        _conkey[0].user.email_confirm= True
        _conkey[0].user.save()
        ctx["message"] = "이메일 인증이 완료 되었습니다. 서비스를 이용해주세요!"
        ctx["error"] = True

        tpl = loader.get_template(TEMP.V2_CONFIRM_RESULT)
        ctx.update(csrf(request))
        return HttpResponse(tpl.render(ctx))


    ctx["message"] = "이메일 인증이 실패 하였습니다. 인증 메일을 다시 보내주세요!"
    ctx["error"] = False
    tpl = loader.get_template(TEMP.V2_CONFIRM_RESULT)
    ctx.update(csrf(request))
    return HttpResponse(tpl.render(ctx))

def send_confirm(request):

    if request.method == "GET":
        send_confirm_form = Send_ConfirmForm()
    elif request.method == "POST":
        print "POST"
        send_confirm_form = Send_ConfirmForm(request.POST)

        if send_confirm_form.is_valid():
            _user = User.objects.filter(username=send_confirm_form.cleaned_data['email'])
            print _user

            if(_user.exists()):
                key = utils.generate_key(32,SignupConfirmKey,_user[0])

                host =request.META['HTTP_HOST']
                title = u"안녕하세요! 토마킷입니다. 정식 사용을 승인해주세요."
                sender = "makerecipe@gmail.com"

                if SET_LOCAL:
                    utils.send_key_email(request, title, sender,
                        _user[0].email, TEMP.V2_CONFIRM_MAIL, key)
                else:
                    tasks.send_key_email.delay(request, title, sender,
                        _user[0].email, TEMP.V2_CONFIRM_MAIL, key)


    return render(request, TEMP.V2_SEND_CONFIRM, {
        "send_conf_for":send_confirm_form,
    })


def pw_reset_request(request):

    if request.method =="GET":
        pwresetform = PwReset_RequestForm()
    elif request.method =="POST":
        pwresetform = PwReset_RequestForm(request.POST)

        if pwresetform.is_valid():
            _user = User.objects.filter(username=pwresetform.cleaned_data['email'])

            if(_user.exists() and _user[0].has_usable_password()):
                key = utils.generate_key(32,PWResetKeys,_user[0])

                host =request.META['HTTP_HOST']
                title = u"안녕하세요. 토마킷 패스워드 변경 이메일을 보내드려요.."
                sender = "makerecipe@gmail.com"

                if SET_LOCAL:
                    utils.send_key_email(request, title, sender,
                        _user[0].email, TEMP.V2_PW_RESET_EMAIL, key)
                else:
                    tasks.send_key_email.delay(request, title, sender,
                        _user[0].email, TEMP.V2_PW_RESET_EMAIL, key)

    return render(request, TEMP.V2_PW_RESET, {
        'pwrsetform':pwresetform
    })

def pw_reset_process(request, key):

    ctx =Context({
        'error':None
    })

    _reset_obj = PWResetKeys.find(key)

    if(_reset_obj == None):
        tpl = loader.get_template(TEMP.V2_PW_RESET_FAIL)
        ctx.update(csrf(request))
        return HttpResponse(tpl.render(ctx))

    if (request.method=="GET"):
        pwresetform = PwReset_ProcessForm()
        return render(request, TEMP.V2_PW_RESET_PROCESS, {
            'pwresetform':pwresetform})

    if (request.method=="POST"):
        pwresetform = PwReset_ProcessForm(request.POST)

        if(not pwresetform.is_valid()):
            return render(request, TEMP.V2_PW_RESET_PROCESS, {
                'pwresetform':pwresetform})

        _user = _reset_obj.user
        _user.set_password(pwresetform.cleaned_data['password'])
        _user.save()
        return HttpResponseRedirect('/v2/user/login')

    pwreset_process_form = PwReset_ProcessForm()
    return render(request, TEMP.V2_PW_RESET_PROCESS, {
        'pwrset_process_form':pwreset_process_form
    })



