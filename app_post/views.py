#coding: utf-8

from django.shortcuts import \
    render,\
    loader
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
    PostCategory, \
    PostType,\
    Post, \
    PostPic, \
    PostDetail
from app_post.form import \
    ClassForm, \
    PostPicForm,  \
    PostdetailForm,\
    KitForm
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
            _type, type_created = PostType.objects.get_or_create(type_name="class")
            if type_created:
                _type.save()

            category_list=[]
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
                except Exception:
                    print Exception.message

                _postpic = PostPic(user=request.user, post=_class,type=_type, post_photo=content)
                _postpic.save()
                for category in category_list:
                    _postpic.category.add(category)
                _postpic.save()

                _post_detail =post_detail_form.save(commit=False)
                _post_detail.type=_type
                _post_detail.user = request.user
                _post_detail.post = _class
                _post_detail.save()
                for category in category_list:
                        _post_detail.category.add(category)
                _post_detail.save()


            return HttpResponseRedirect('/post/class/{0}'.format(_class.id))

    return render(request, 'app_class/create_class_post.html',
        {
            'class_createform':class_form,
            'classpic_createform':post_pic_form,
            'class_detailform': post_detail_form,
        })

@login_required
def kitcreate(request):

    ctx = Context({
        'error':None
    })
    error = False

    if request.method == "GET":
        kit_form=KitForm()
        pic_form=PostPicForm()
        detail_form = PostdetailForm()
    elif request.method == "POST":
        kit_form = KitForm(request.POST)
        pic_form = PostPicForm(request.FILES)
        detail_form = PostdetailForm(request.POST)

        u_categorys = request.POST.getlist(u'category')
        photos =request.FILES.getlist("kit_photo")


        for photo in photos:
            if photo.content_type != 'image/png' and photo.content_type !='image/jpeg':
                pic_form.add_error('kit_photo', u'jpeg와 png형식의 이미지만 가능합니다.')
                print "error"
                error =True

        #start make post
        if kit_form.is_valid() and not error and detail_form.is_valid():
            _type, type_created = PostType.objects.get_or_create(type_name="kit")
            if type_created:
                _type.save()

            category_list=[]
            for category in u_categorys:
                _category, categ_created = PostCategory.objects.get_or_create(category_name=category)
                if categ_created:
                    _category.save()
                category_list.append(_category)

            _kit = kit_form.save(commit=False)
            _kit.type = _type
            _kit.user = request.user
            _kit.save()
            for category in category_list:
                _kit.category.add(category)
            _kit.save()

            for photo in photos:
                try :
                    t = handle_uploaded_image(photo, 500, 500)
                    content = t[1]
                except Exception:
                    print Exception.message
                _postpic = PostPic(user=request.user, post=_kit, type=_type, post_photo=content)
                _postpic.save()
                for category in category_list:
                    _postpic.category.add(category)
                _postpic.save()

                _post_detail =detail_form.save(commit=False)
                _post_detail.type=_type
                _post_detail.user = request.user
                _post_detail.post = _kit
                _post_detail.save()
                for category in category_list:
                        _post_detail.category.add(category)
                _post_detail.save()

            return HttpResponseRedirect('/post/kit/{0}'.format(_kit.id))

    return render(request, 'app_kit/create_kit_post.html',
        {
            'kit_createform':kit_form,
            'kit_pic_createform':pic_form,
            'kit_detailform': detail_form,
        })



def class_detail(request, class_num):

    ctx = Context({
        'error':None
    })
    error = False

    if request.method == "GET":
        try:
            _class_post = Post.objects.get(pk=class_num)
        except _class_post.DoesNotExist:
            raise Http404("post does not exist")
    return render(request, 'app_class/class_post.html',
        {
            'class_post':_class_post
        })

def kit_detail(request, kit_num):

    ctx = Context({
        'error':None
    })
    error = False
    if request.method == "GET":
        try:
            _kit_post = Post.objects.get(pk=kit_num)

        except _kit_post.DoesNotExist:
            raise Http404("post does not exist")
    return render(request, 'app_kit/kit_post.html',
        {
            'kit_post':_kit_post
        })

def handler404(request):

    template = loader.get_template('error/404.html')
    context = Context({
        'message': 'HTTP 404:: 잘못된 주소입니다.',
    })

    return HttpResponse(content = template.render(context),
                        content_type='text/html; charset=utf-8', status=404)

def handler500(request):
    template = loader.get_template('error/500.html')
    context = Context({
        'message':'HTTP 500:: 서버 에러 입니다.',
    })

    return HttpResponse(content=template.render(context),
                        content_type='text/html; charset=utf-8', status=500)