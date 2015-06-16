#coding: utf-8
from django.shortcuts import \
    render, \
    loader
from django.contrib.auth import \
    get_user_model,\
    authenticate, \
    login as authlogin
from django.contrib.auth.views import \
    login as django_login,\
    logout as django_logout
from django.contrib.auth.decorators import \
    login_required
from django.http import \
    HttpResponseRedirect, \
    HttpResponse
from django.core.mail import\
    send_mail
from django.template import\
    Context
from django.core.context_processors import \
    csrf
import os
from django.core.files.images import \
    ImageFile

from userapp.models import \
    Profile, \
    SignupConfirmKey, \
    PasswordResetKeys, \
    SellerInfo

from userapp.form import \
    ProfilesForm, \
    PwReset_RequestForm, \
    PwReset_ProcessForm, \
    LoginForm,\
    SendEmailForm

from userapp import tasks
from userapp.utils import handle_uploaded_image
from DIY_tool import settings


Local=True
# Create your views here.
def signup(request):
    print "signup"
    ctx = Context({
        'error':None
    })
    next=""
    if request.method == "GET":
        profile_form = ProfilesForm()
        next=request.GET.get("next", "/")

    elif request.method =="POST" :
        print "signup post"
        profile_form = ProfilesForm(request.POST, request.FILES)

        if profile_form.is_valid():
            print "test:: signup valid"
            valid_error = False
            email = request.POST['email'].strip()
            password = request.POST['password']
            password_confirm = request.POST['password_confirm']
            nick_name = request.POST['nick_name']
            next=request.POST.get("next","/")
            print next

            if password != password_confirm:
                profile_form.add_error('password','비밀번호가 일치하지 않습니다. 정확히 입력해주세요.')
                valid_error =True

            #upload image or user defualt
            if bool(request.FILES):
                image_type = request.FILES['pro_photo'].content_type
                if image_type != 'image/png' and image_type !='image/jpeg':
                    print "error"
                    profile_form.add_error('pro_photo','jpg와 png 형식의 이미지만 가능합니다.')
                    valid_error =True
                try :
                    t = handle_uploaded_image(request.FILES['pro_photo'], 50, 50)
                    content = t[1]
                except :
                    image_file = open(os.path.join(settings.BASE_DIR,
                                               'resource/image/default_profile.jpg'),'r')
                    content = ImageFile(image_file)
            else :
                image_file = open(os.path.join(settings.BASE_DIR,
                                               'resource/image/default_profile.jpg'),'r')
                content = ImageFile(image_file)


            if valid_error:
                return render(request, 'userapp/signup.html',{
                    'profileform':profile_form,},
                  )

            User = get_user_model()
            _u = User(username = email)
            _u.set_password(password)
            _u.save()
            #chang form
            _profile = Profile(user = _u, email = email,pro_photo=content, nick_name=nick_name)
            _profile.save()

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

            if Local:
                #sendmail not celery
                from django.core.mail import send_mail
                send_mail(u'안녕하세요! 앞발 사용 설명서입니다. 정식 사용을 승인해주세요.', "", \
                          'makerecipe@gmail.com', recipient, fail_silently=False,
                            html_message=cont)
            else:
                tasks.sendmail.delay(cont, recipient)



        return HttpResponseRedirect("/user/login/?next="+next)

    return render(request, 'userapp/signup.html',{
                    'profileform':profile_form,
                    'next':next,},)


def sellersignup(request):
    ctx = Context({
        'error':None
    })
    next=""
    if request.method == "GET":
        profile_form = ProfilesForm()
        next=request.GET.get("next", "/")

    elif request.method =="POST" :
        profile_form = ProfilesForm(request.POST, request.FILES)

        if profile_form.is_valid():
            valid_error = False
            email = request.POST['email'].strip()
            password = request.POST['password']
            password_confirm = request.POST['password_confirm']
            nick_name = request.POST['nick_name']
            next=request.POST.get("next","/")
            intro=request.POST['special']
            special=request.POST['intro']

            if password != password_confirm:
                profile_form.add_error('password','비밀번호가 일치하지 않습니다. 정확히 입력해주세요.')
                valid_error =True

            #upload image or user defualt
            if bool(request.FILES):
                image_type = request.FILES['pro_photo'].content_type
                if image_type != 'image/png' and image_type !='image/jpeg':
                    print "error"
                    profile_form.add_error('pro_photo','jpg와 png 형식의 이미지만 가능합니다.')
                    valid_error =True
                try :
                    t = handle_uploaded_image(request.FILES['pro_photo'], 50, 50)
                    content = t[1]
                except :
                    image_file = open(os.path.join(settings.BASE_DIR,
                                               'resource/image/default_profile.jpg'),'r')
                    content = ImageFile(image_file)
            else :
                image_file = open(os.path.join(settings.BASE_DIR,
                                               'resource/image/default_profile.jpg'),'r')
                content = ImageFile(image_file)


            if valid_error:
                return render(request, 'userapp/signup.html',{
                    'profileform':profile_form,},
                  )

            User = get_user_model()
            _u = User(username = email)
            _u.set_password(password)
            _u.save()
            #chang form
            _profile = Profile(user = _u, email = email,pro_photo=content, nick_name=nick_name)
            _profile.save()

            #seller info
            _seinfo=SellerInfo(user=_profile,intro=intro, special=special)
            _seinfo.save()

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

            if Local:
                #sendmail not celery
                from django.core.mail import send_mail
                send_mail(u'안녕하세요! 앞발 사용 설명서입니다. 정식 사용을 승인해주세요.', "", \
                          'makerecipe@gmail.com', recipient, fail_silently=False,
                            html_message=cont)
            else:
                tasks.sendmail.delay(cont, recipient)

            return HttpResponseRedirect("/user/login/?next="+next)

    return render(request, 'userapp/sellersignup.html',{
                    'profileform':profile_form,
                    'next':next,},)


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

                if Local:
                    pass
                else:
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

    next=""
    if request.method=="GET":
        print "login get"
        login_form = LoginForm(None)
        next=request.GET.get("next","/")

    elif request.method=="POST":
        print "login post"
        login_form = LoginForm(request.POST)
        next=request.POST.get("next","/")
        print next
        if login_form.is_valid():
            user = login_form.login(request)
            if user:
                authlogin(request, user)
                return HttpResponseRedirect(next)

    return render(request, 'userapp/login.html',
                  {'login_form':login_form,
                   'next':next
                   })

def logout(request, *args, **kwargs):
    res = django_logout(request, *args, **kwargs)
    print request.path
    return res

@login_required
def profile(request, *args, **kwargs):

    ctx = Context({
        'error':None
    })
    user = request.user

    _profile = Profile.objects.filter(email = user)
    ctx['profile']= _profile[0]

    #tpl = loader.get_template('userapp/profile.html')
    #ctx.update(csrf(request))
    return render(request, 'userapp/profile.html',{
                    'profile':_profile[0],
                    },)

@login_required
def contactemail(request):
    if request.method=="GET":
        email_form = SendEmailForm()
    elif request.method=="POST":
        email_form=SendEmailForm(request.POST)
        customer_address=request.POST["from_address"]
        content=request.POST["content"]
        username=request.user

        if email_form.is_valid():
            #write email
            tpl_mail = loader.get_template('mail_form/mail_contact.html')
            ctx_mail = Context({
                'address':customer_address,
                'content':content,
                'user':username
            })
            cont = tpl_mail.render(ctx_mail)
            recipient = ["makerecipe@gmail.com"]


            if Local:
                from django.core.mail import send_mail
                send_mail(u'안녕하세요! 앞발 사용 설명서입니다. 정식 사용을 승인해주세요.', "", \
                          'makerecipe@gmail.com', recipient, fail_silently=False,
                            html_message=cont)
            else:
                tasks.contact_mail.delay(cont, recipient)

            # tasks.rabbitmqtest.delay()

    return render(request, 'userapp/partnershipmail.html',{
        'emailform' : SendEmailForm

    })

def userprivacy(request):

    return render(request, 'userapp/userprivacy.html', {
    })