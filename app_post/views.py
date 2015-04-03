#coding: utf-8

from django.shortcuts import render
from django.contrib.auth.decorators import \
    login_required
from django.template import\
    Context
from django.http import \
    HttpResponseRedirect,\
    HttpResponse, \
    Http404
import datetime


from app_post.models import \
    PostType, \
    PostCategory, \
    Post, \
    PostPic, \
    PostDetail
from app_post.form import \
    ClassForm, \
    PostPicForm,  \
    PostdetailForm
from userapp.utils import handle_uploaded_image

@login_required
def classcreate(request):

    ctx = Context({
        'error':None
    })
    error = False

    if request.method == "GET":
        class_form =ClassForm()
        post_pic_form = PostPicForm()
        post_detail_form = PostdetailForm()


    elif request.method =="POST":
        class_form = ClassForm(request.POST)
        post_pic_form = PostPicForm(request.FILES)
        post_detail_form = PostdetailForm(request.POST)



        u_categorys = request.POST.getlist(u'category')
        u_day = request.POST['lessonday']
        u_start_time = request.POST['start_time']
        u_end_time = request.POST['end_time']

        u_min_num = request.POST['minimum']
        u_max_num = request.POST['maximum']

        #read photo
        photos =request.FILES.getlist("class_photo")


        for photo in photos:
            if photo.content_type != 'image/png' and photo.content_type !='image/jpeg':
                post_pic_form.add_error('class_photo', u'jpeg와 png형식의 이미지만 가능합니다.')
                print "error"
                error =True

        if class_form.is_valid() and not error:
            start_time =datetime.datetime.strptime(u_start_time, '%H:%M')
            end_time = datetime.datetime.strptime(u_end_time, '%H:%M')

            if start_time > end_time:
                class_form.add_error('start_time', u'시작 시간은 끝나는 시간보다 빨라야 합니다.')
                error =True

        if class_form.is_valid() and not error:
            if u_min_num > u_max_num:
                class_form.add_error('minimum', u'최소인원은 최대 인원보다 많아야 합니다.')
                error =True

        #start make post
        if class_form.is_valid() and not error and post_detail_form.is_valid():
            category_list=[]
            _type, type_created = PostType.objects.get_or_create(type_name="class")
            if type_created:
                _type.save()

            for category in u_categorys:
                _category, categ_created = PostCategory.objects.get_or_create(category_name=category)
                if categ_created:
                    _category.save()
                category_list.append(_category)

            _class = class_form.save(commit=False)
            _class.user = request.user
            _class.type = _type
            day= datetime.datetime.strptime(u_day, '%Y-%m-%d')
            _class.lessonday = day
            _class.start_time = start_time
            _class.end_time = end_time
            _class.save()
            for category in category_list:
                _class.category.add(category)
            _class.save()

            for photo in photos:
                try :
                    t = handle_uploaded_image(photo, 500, 500)
                    content = t[1]
                    print content
                except Exception:
                    print Exception.message

                _postpic = PostPic(user=request.user, post=_class,type=_type, post_photo=content)
                _postpic.save()
                print _postpic
                for category in category_list:
                    _postpic.category.add(category)
                _postpic.save()

                _class_detail =post_detail_form.save(commit=False)
                _class_detail.type=_type
                _class_detail.user = request.user
                _class_detail.post = _class
                _class_detail.save()
                for category in category_list:
                        _class_detail.category.add(category)
                _class_detail.save()


            return HttpResponseRedirect('/class/{0}'.format(_class.id))

    return render(request, 'app_class/create_class_post.html',
        {
            'class_createform':class_form,
            'classpic_createform':post_pic_form,
            'class_detailform': post_detail_form,
        })


def class_detail(request, class_num):

    ctx = Context({
        'error':None
    })
    error = False

    if request.method == "GET":
        try:
            _class_post = Post.objects.filter
        except _class_post.DoesNotExist:
            raise Http404("Class does not exist")
    return render(request, 'app_class/class_post.html',
        {
            'class_post':_class_post
        })
