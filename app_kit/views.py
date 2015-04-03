#coding: utf-8

from django.shortcuts import render
from django.http import \
    HttpResponseRedirect,\
    HttpResponse, \
    Http404
from django.template import\
    Context
from django.contrib.auth.decorators import \
    login_required

from app_kit.form import \
    KitCreateForm, \
    KitDetailForm, \
    KitPicCreateForm
from app_kit.models import \
    Kit_Post,\
    Kit_Photo, \
    Kit_Detail
from userapp.utils import \
    handle_uploaded_image
# Create your views here.

@login_required
def kitcreate(request):

    ctx = Context({
        'error':None
    })
    error = False

    if request.method == "GET":
        kit_form=KitCreateForm()
        kitpic_form=KitPicCreateForm()
        kit_detail_form = KitDetailForm()
    else:
        kit_form = KitCreateForm(request.POST)
        kitpic_form = KitPicCreateForm(request.FILES)
        kit_detail_form = KitDetailForm(request.POST)

        #read photo
        photos =request.FILES.getlist("kit_photo")


        for photo in photos:
            if photo.content_type != 'image/png' and photo.content_type !='image/jpeg':
                kitpic_form.add_error('kit_photo', u'jpeg와 png형식의 이미지만 가능합니다.')
                print "error"
                error =True

        #start make post
        if kit_form.is_valid() and not error and kit_detail_form.is_valid():
            _kit = kit_form.save(commit=False)
            _kit.user = request.user
            _kit.save()

            for photo in photos:
                try :
                    t = handle_uploaded_image(photo, 500, 500)
                    content = t[1]
                    _kitpic = Kit_Photo(user=request.user, kit_post=_kit, kit_photo=content)
                    _kitpic.save()
                except Exception:
                    print Exception.message
                _kit_detail =kit_detail_form.save(commit=False)
                _kit_detail.user = request.user
                _kit_detail.kit_post = _kit
                _kit_detail.save()

            return HttpResponseRedirect('/kit/{0}'.format(_kit.id))

    return render(request, 'app_kit/create_kit_post.html',
        {
            'kit_createform':kit_form,
            'kit_pic_createform':kitpic_form,
            'kit_detailform': kit_detail_form,
        })

def kit_detail(request, kit_num):

    ctx = Context({
        'error':None
    })
    error = False
    if request.method == "GET":
        try:
            _kit_post = Kit_Post.objects.get(pk=kit_num)

        except Kit_Post.DoesNotExist:
            raise Http404("kit does not exist")
    return render(request, 'app_kit/kit_post.html',
        {
            'kit_post':_kit_post
        })