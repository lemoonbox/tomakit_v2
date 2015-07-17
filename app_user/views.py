#coding:utf-8
from django.shortcuts import render
from django.template import \
    Context
from django.shortcuts import \
    render
from django.contrib.auth.models import \
    User
from django.http import \
    HttpResponseRedirect
import \
    string, \
    random
from django.shortcuts import \
    loader,\
    render

from DIY_tool import \
    template_match as TEMP
from DIY_tool.settings import \
    LOCAL as SET_LOCAL
from utils import tasks
from app_user.form import \
    UserForm
from app_user.models import \
    UserProfile, \
    SignupConfirmKey
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
                key=""

                while True:
                    for i in xrange(32):
                        key = key+random.choice(string.ascii_letters\
                            +string.digits)
                    if (SignupConfirmKey.find(key)==None):break

                _conkey = SignupConfirmKey(key=key, user=_user)
                _conkey.save()

                host=request.META['HTTP_HOST']
                mail_tpl = loader.get_template('contents/mail_form/mail_confirm.html')
                mail_ctx = Context({'host':host, 'key':key})
                cont = mail_tpl.render(mail_ctx)
                recipient = [_user.email]

                if SET_LOCAL:
                    from django.core.mail import send_mail
                    send_mail(u'안녕하세요! 토마킷입니다. 정식 사용을 승인해주세요.', "", \
                          'makerecipe@gmail.com', recipient, fail_silently=False,
                            html_message=cont)

                else:
                    tasks.sendmail.delay(cont, recipient)

                return HttpResponseRedirect("/v2/user/login/?next="+next)

    return render(request, TEMP.V2_SIGNUP_TEM,{
        'accountform':userForm,
        'next':next,})
