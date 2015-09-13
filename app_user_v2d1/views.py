#coding: utf-8
import os
from django.core.files.images import \
    ImageFile
from django.shortcuts import \
    render, \
    loader
from django.contrib.auth.models import \
    User
from django.http import \
    HttpResponse, \
    HttpResponseRedirect
from django.contrib.auth import \
    login as auth_login
from django.contrib.auth import \
    authenticate
from django.template import \
    Context
from django.core.context_processors import \
    csrf
from django.contrib.auth.views import \
    logout as django_logout

from DIY_tool import \
    template_match as TEMP, \
    settings
from DIY_tool.settings import LOCAL as SET_LOCAL

from app_user_v2d1.forms import\
    UserForm,\
    LoginForm, \
    EmailCheck,\
    PW_CrossCheckForm
from app_user_v2d1.models import \
    T2Profile, \
    T2SignupConfirmKey,\
    T2PWResetKeys

from utils import \
    utils, \
    tasks
# Create your views here.


def signup(request):
    next=""
    HTTP_HOST=request.META["HTTP_HOST"]
    if request.method == "GET":
        userForm=UserForm()
        next=request.GET.get("next", "/")
    elif request.method == "POST":
        next=request.POST.get("next", "/")
        username=request.POST.get("username", "nodata")
        email=request.POST.get("username", "nodata")
        first_name=request.POST.get("first_name", "nodata")
        last_name=request.POST.get("last_name", "nodata")
        password=request.POST.get("password", "nodata")

        userForm=UserForm(request.POST)
        if userForm.is_valid():
            user_data={
                'username':username,
                'email':email,
                'first_name':first_name,
                'last_name':last_name,
                'password':password,
            }
            _user=User.objects.create_user(**user_data)
            _user.save()
            image_file=open(os.path.join(
                    settings.BASE_DIR,'resource/image/default_prof.png'), 'r')
            content=ImageFile(image_file)
            _profile=T2Profile(user=_user, pro_pic=content)
            _profile.save()

            _able_user = authenticate(username=username, password=password)
            if _able_user:
                auth_login(request, _able_user)
            #send mail
            key = utils.generate_key(32, T2SignupConfirmKey, _user)
            title = u"안녕하세요! 토마킷입니다. 정식 사용을 승인해주세요."
            sender = "tomakit.info@gmail.com"

            if SET_LOCAL:
               utils.send_key_email(request, title, sender,
                    _user.email, TEMP.CONFRI_TEM_V2D1, key)
            else:
                tasks.send_key_email.delay(HTTP_HOST, title, sender,
                _user.email, TEMP.CONFRI_TEM_V2D1, key)
            return HttpResponseRedirect(next)

    return render(request, TEMP.SIGNUP_TEM_V2D1,{
        'accountform':userForm,
        'next':next,
        'HTTP_HOST':HTTP_HOST,
        })


def login(request, *args, **kwargs):

    next=""
    HTTP_HOST = request.META["HTTP_HOST"]
    if request.method=="GET":
        login_form = LoginForm()
        next=request.GET.get("next","/")

    elif request.method=="POST":
        login_form = LoginForm(request.POST)
        next=request.POST.get("next", "/")
        if login_form.is_valid():
            user = login_form.authenticate(request)
            if user:
                auth_login(request, user)
                return HttpResponseRedirect(next)

    return render(request, TEMP.V2_LOGIN,
                  {'login_form':login_form,
                   'next':next,
                    'HTTP_HOST':HTTP_HOST,
                   })
def logout(request, *args, **kwargs):
    res = django_logout(request, *args, **kwargs)
    return res

def send_confirm(request):

    if request.method == "GET":
        email_form = EmailCheck()
    elif request.method == "POST":
        email_form = EmailCheck(request.POST)

        if not email_form.is_valid():
            _user = User.objects.filter(username=email_form.data['username'])
            if(_user):
                key = utils.generate_key(32,T2SignupConfirmKey,_user[0])
                host =request.META['HTTP_HOST']
                title = u"아래의 링크를 클릭하시면 비밀번호를 변경하실 수 있습니다."
                sender = "tomakit.info@gmail.com"

                if SET_LOCAL:
                    utils.send_key_email(request, title, sender,
                        _user[0].email, TEMP.CONFRI_TEM_V2D1, key)
                else:
                    tasks.send_key_email.delay(host, title, sender,
                        _user[0].email, TEMP.CONFRI_TEM_V2D1, key)
        else:
            print "not eixst"
            email_form.add_error("username", "존재 하지 않는 이메일 입니다.")



    HTTP_HOST = request.META["HTTP_HOST"]
    return render(request, TEMP.SEND_CONFRI_TEM_V2D1, {
        "email_form":email_form,
        'HTTP_HOST':HTTP_HOST,

    })


def signup_confirm(request, *args, **kwargs):

    HTTP_HOST = request.META["HTTP_HOST"]
    ctx = Context({
        'error':None,
        'host':HTTP_HOST,

    })

    _conkey = T2SignupConfirmKey.find(kwargs['key'])

    if(_conkey):
        _profile=_conkey[0].user.t2profile_set.first()
        _profile.mail_conf= True
        _profile.save()
        ctx["message"] = "이메일 인증이 완료 되었습니다. 서비스를 이용해주세요!"
        ctx["error"] = True

        tpl = loader.get_template(TEMP.CONFRI_RESULT_TEM_V2D1)
        ctx.update(csrf(request))
        return HttpResponse(tpl.render(ctx))


    ctx["message"] = "이메일 인증이 실패 하였습니다. 인증 메일을 다시 보내주세요!"
    ctx["error"] = False
    tpl = loader.get_template(TEMP.CONFRI_RESULT_TEM_V2D1)
    ctx.update(csrf(request))
    return HttpResponse(tpl.render(ctx))

def pw_reset_request(request):

    HTTP_HOST = request.META["HTTP_HOST"]
    if request.method =="GET":
        pwresetform = EmailCheck()
    elif request.method =="POST":
        pwresetform = EmailCheck(request.POST)

        if not pwresetform.is_valid():
            _user = User.objects.filter(username=pwresetform.data['username'])

            if(_user and _user[0].has_usable_password()):
                key = utils.generate_key(32,T2PWResetKeys,_user[0])

                title = u"안녕하세요. 토마킷 패스워드 변경 이메일을 입니다.."
                sender = "tomakit.info@gmail.com"

                if SET_LOCAL:
                    utils.send_key_email(request, title, sender,
                        _user[0].email, TEMP.PWRESET_MAIL_TEM_V2D1, key)
                else:
                    tasks.send_key_email.delay(HTTP_HOST, title, sender,
                        _user[0].email, TEMP.PWRESET_MAIL_TEM_V2D1, key)

    HTTP_HOST = request.META["HTTP_HOST"]
    return render(request, TEMP.PW_RESET_V2D1, {
        'pwrsetform':pwresetform,
        'HTTP_HOST':HTTP_HOST,

    })


def pw_reset_process(request, key):

    ctx =Context({
        'error':None
    })
    HTTP_HOST = request.META["HTTP_HOST"]
    _reset_obj = T2PWResetKeys.find(key)

    if(_reset_obj == None):
        tpl = loader.get_template(TEMP.PW_RESET_FAIL_V2D1)
        ctx.update(csrf(request))
        return HttpResponse(tpl.render(ctx))

    if (request.method=="GET"):
        pwresetform = PW_CrossCheckForm()
        return render(request, TEMP.PW_RESET_PROCESS_V2D1, {
            'pwresetform':pwresetform})

    if (request.method=="POST"):
        pwresetform = PW_CrossCheckForm(request.POST)

        if(not pwresetform.is_valid()):
            print "not valid"
            return render(request, TEMP.PW_RESET_PROCESS_V2D1, {
                'pwresetform':pwresetform,
                'HTTP_HOST':HTTP_HOST,
                })

        _user = _reset_obj.user
        _user.set_password(pwresetform.cleaned_data['password'])
        _user.save()
        return HttpResponseRedirect('/v2.1/user/login')

    pwreset_process_form = PW_CrossCheckForm()
    return render(request, TEMP.V2_PW_RESET_PROCESS, {
        'pwrset_process_form':pwreset_process_form,
        'HTTP_HOST':HTTP_HOST,
    })