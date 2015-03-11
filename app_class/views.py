#coding: utf-8
from django.shortcuts import \
    render, \
    render_to_response

from django.http import \
    HttpResponseRedirect,\
    HttpResponse, \
    Http404

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
    ClassPicCreateForm,\
    ClassdetailForm

from app_class.models import \
    ClassPic, \
    ClassPost, \
    ClassDetail

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
        class_detail_form = ClassdetailForm()


    elif request.method =="POST":

        class_form = ClassCreateForm(request.POST)
        classpic_form = ClassPicCreateForm(request.FILES)
        class_detail_form = ClassdetailForm(request.POST)


        u_day = request.POST['lessonday']
        u_start_time = request.POST['start_time']
        u_end_time = request.POST['end_time']

        #read photo
        photos =request.FILES.getlist("class_photo")


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

        #start make post
        if class_form.is_valid() and not error and class_detail_form.is_valid():
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

                _class_detail =class_detail_form.save(commit=False)
                _class_detail.user = request.user
                _class_detail.class_post = _class
                _class_detail.save()

            return HttpResponseRedirect('/class/{0}'.format(_class.id))

    return render(request, 'app_class/create_class_post.html',
        {
            'class_createform':class_form,
            'classpic_createform':classpic_form,
            'class_detailform': class_detail_form,
        })

def class_detail(request, class_num):

    ctx = Context({
        'error':None
    })
    error = False
    #class_num이 없거나 있어도 읽어 올 수 없는 경우 처리

    if request.method == "GET":

        try:
            _class_post = ClassPost.objects.get(pk=class_num)
        except ClassPost.DoesNotExist:
            raise Http404("Class does not exist")
    return render(request, 'app_class/class_post.html',
        {
            'class_post':_class_post
        })



def handler404(request):

    template = loader.get_template('error/404.html')
    context = Context({
        'message':'All:%s'%request,
    })

    return HttpResponse(contet = template.render(context),
                        content_type='text/html; charset=utf-8', status=404)

def handler500(request):
    template = loader.get_template('error/500.html')
    context = Context({
        'message':'All:%s'%request,
    })

    return HttpResponse(content=template.render(context),
                        content_type='text/html; charset=utf-8', status=404)