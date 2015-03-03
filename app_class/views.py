#coding: utf-8
from django.shortcuts import \
    render
from django.http import \
    HttpResponseRedirect,\
    HttpResponse
from django.core.context_processors import \
    csrf
from django.shortcuts import \
    render, \
    loader
from django.template import\
    Context
from django.contrib.auth.decorators import \
    login_required
from django.shortcuts import \
    get_object_or_404



from app_class.form import \
    ClassCreateForm,\
    ClassPicCreateForm

from app_class.models import \
    ClassPic, \
    ClassPost
from userapp.utils import \
    handle_uploaded_image
import datetime

from userapp.utils import handle_uploaded_image

# Create your views here.

@login_required
def classcreate(request):

    ctx = Context({
        'error':None
    })
    error = False

    if request.method == "GET":
        class_form =ClassCreateForm()
        classpic_form = ClassPicCreateForm()

    elif request.method =="POST":

        class_form = ClassCreateForm(request.POST)
        classpic_form = ClassPicCreateForm(request.FILES)

        host = request.META['HTTP_HOST']
        u_day = request.POST['lessonday']
        u_start_time = request.POST['start_time']
        u_end_time = request.POST['end_time']

        #read photo
        photos =request.FILES.getlist("class_photo")

        print classpic_form.is_valid()

        for photo in photos:
            if photo.content_type != 'image/png' and photo.content_type !='image/jpeg':
                classpic_form.add_error('class_photo', u'jpeg와 png형식의 이미지만 가능합니다.')
                print "error"
                error =True

        if class_form.is_valid() and not error:
            start_time =datetime.datetime.strptime(u_start_time, '%H:%M')
            end_time = datetime.datetime.strptime(u_end_time, '%H:%M')

            if start_time > end_time:
                class_form.add_error('start_time', u'시작 시간은 끝나는 시간보다 빨라야 합니다.')
                error =True


        if class_form.is_valid() and not error:
            _class = class_form.save(commit=False)
            _class.user = request.user
            day= datetime.datetime.strptime(u_day, '%Y-%m-%d')

            _class.lessonday = day
            _class.start_time = start_time
            _class.end_time = end_time
            _class.save()

            for photo in photos:
                try :
                    t = handle_uploaded_image(photo, 500, 500)
                    content = t[1]
                    _classpic = ClassPic(user=request.user, class_post=_class, class_photo=content)
                    _classpic.save()
                except Exception:
                    print Exception.message

            return HttpResponseRedirect('http://{0}/user/profile'.format(host))

    return render(request, 'app_class/create_class_post.html',
        {
            'class_createform':class_form,
            'classpic_createform':classpic_form
        })

def class_detail(request, class_num):

    ctx = Context({
        'error':None
    })
    error = False

    print class_num
    #class_num이 없거나 있어도 읽어 올 수 없는 경우 처리

    if request.method == "GET":
        _class_detail = get_object_or_404(ClassPost, pk=class_num)


    tpl = loader.get_template('app_class/class_detail.html')
    ctx.update(csrf(request))
    return render(request, 'app_class/class_detail.html',
        {
            'class_detial':_class_detail
        })