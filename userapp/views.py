#coding: utf-8
from django.shortcuts import render, loader
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.views import login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.template import Context
from django.core.context_processors import csrf

from userapp.models import Profile, SignupConfirmKey, PasswordResetKeys
from userapp.form import ProfilesForm, PwReset_RequestForm, PwReset_ProcessForm
from userapp import tasks

# Create your views here.

def signup(request):

    ctx = Context({
        'error':None
    })
    if request.method == "GET":
        profile_form = ProfilesForm()

    elif request.method =="POST" :


        print request.FILES
        print type(request.FILES)
        print request.FILES['pro_photo']
        print type(request.FILES['pro_photo'])

        profile_form = ProfilesForm(request.POST)

        email = request.POST['email'].strip()
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        mobile =  request.POST['mobile']
        address = request.POST['address']
        #이미지 파일 업로드 되지 않는 경우 처리해함.
        filename = request.FILES['pro_photo']


        if profile_form.is_valid():
            if password != password_confirm:
                profile_form.add_error('password','비밀번호가 일치 하지 않음')
                print "thumnail test"

            else :
                User = get_user_model()
                _u = User(username = email)
                _u.set_password(password)
                _u.save()
                _profile = profile_form.save(commit=False)
                _profile.user =_u
                _profile.save()

                #make thumnail
                from PIL import Image
                image = Image.


                #send_email confirm
                import string , random
                key =""

                while True:
                    for i in xrange(32):
                        key = key+random.choice(string.ascii_letters\
                            +string.digits)

                    if (SignupConfirmKey.find(key)==None):break

                #save the key
                conkey = SignupConfirmKey(key=key, user=_profile)
                conkey.save()

                host = request.META['HTTP_HOST']

                #write email
                tpl_mail = loader.get_template('mail_form/mail_confirm.html')
                ctx_mail = Context({
                    'host':host,
                    'key':key,
                })
                cont = tpl_mail.render(ctx_mail)
                recipient = [_profile.email]

                """

                tasks.sendmail.delay(cont, recipient)

                #sendmail net celery
                from django.core.mail import send_mail
                send_mail(u'안녕하세요! 앞발 사용 설명서입니다. 정식 사용을 승인해주세요.', "", \
                          'makerecipe@gmail.com', recipient, fail_silently=False,
                            html_message=cont)
                """



                return HttpResponseRedirect("user/login/")

    return render(request, 'userapp/signup.html',{
                    'profileform':profile_form,},
                  )


def signup_confirm(request, *args, **kwargs):

    ctx = Context({
        'error':None
    })
    ctx["host"] = request.META['HTTP_HOST']

    _conkey = SignupConfirmKey.find(kwargs['key'])

    if(_conkey):
        _conkey[0].user.email_confirm= True
        ctx["message"] = "이메일 인증이 완료 되었습니다. 서비스를 이용해주세요!"
        ctx["error"] = True

        tpl = loader.get_template('userapp/confirm_result.html')
        ctx.update(csrf(request))
        return HttpResponse(tpl.render(ctx))


    ctx["message"] = "이메일 인증이 실패 하였습니다. 인증메일을 다시 보내주세요!"
    ctx["error"] = False
    tpl = loader.get_template('userapp/confirm_result.html')
    ctx.update(csrf(request))
    return HttpResponse(tpl.render(ctx))

def pw_reset_request(request):

    if (request.method == "POST"):
        pwresetform = PwReset_RequestForm(request.POST)

        if(pwresetform.is_valid()):
            USER_model = get_user_model()
            _u = USER_model.objects.filter(username= pwresetform.cleaned_data['email'])

            if (_u.exists()):

                import string, random
                key = ""

                while True :

                    for i in xrange(32):
                        key = key + random.choice(string.ascii_letters\
                            +string.digits)

                    #check repetition
                    if(PasswordResetKeys.find(key)==None):break

                pkey = PasswordResetKeys(key=key, user=_u[0])
                pkey.save()

                host = request.META['HTTP_HOST']

                #wirte email
                tpl_mail = loader.get_template('mail_form/pw_chang.html')
                ctx_mail = Context({
                    'host':host,
                    'key':key,
                })
                cont = tpl_mail.render(ctx_mail)

                recipient = [_u[0].username]
                print _u[0].username

                tasks.send_pwchang_mail.delay(cont, recipient)

    pwresetform = PwReset_RequestForm()
    return render(request, 'userapp/pw_reset.html', {
        'pwrsetform':pwresetform
    })

def pw_reset_process(request, key):

    ctx =Context({
        'error':None
    })

    _reset_obj = PasswordResetKeys.find(key)

    if(_reset_obj == None):
        tpl = loader.get_template('userapp/pw_reset_fail.html')
        ctx.update(csrf(request))
        return HttpResponse(tpl.render(ctx))

    if (request.method=="GET"):
        pwresetform = PwReset_ProcessForm()

        return render(request, 'userapp/pw_reset_process.html', {
            'pwresetform' : pwresetform
        })

    if (request.method=="POST"):
        pwresetform = PwReset_ProcessForm(request.POST)

        if( not pwresetform.is_valid()):
            return render(request, 'userapp/pw_reset_process.html', {
            'pwresetform' : pwresetform})


        if(pwresetform.cleaned_data['password'] != pwresetform.cleaned_data['password_confirm']):
            pwresetform.add_error('password_confirm', u'비밀 번호가 일치하지 않습니다.')
            return render(request, 'userapp/pw_reset_process.html', {
                'pwresetform' : pwresetform})

        _u = _reset_obj.user
        _u.set_password(pwresetform.cleaned_data['password'])
        _u.save()
        return HttpResponseRedirect('user/login')

    pwreset_process_form = PwReset_ProcessForm()
    return render(request, 'userapp/pw_reset_process.html', {
        'pwrset_process_form':pwreset_process_form
    })





def login(request, *args, **kwargs):
    print args
    print kwargs
    res = django_login(request, *args, **kwargs)
    return res

def logout(request, *args, **kwargs):
    res = django_logout(request, *args, **kwargs)
    return res

@login_required
def profile(request, *args, **kwargs):

    print args
    print kwargs

    ctx = Context({
        'error':None
    })
    user = request.user
    _profile = Profile.objects.filter(email = user)

    print _profile[0].email

    ctx['profile']= _profile[0]

    tpl = loader.get_template('userapp/profile.html')
    return HttpResponse(tpl.render(ctx))