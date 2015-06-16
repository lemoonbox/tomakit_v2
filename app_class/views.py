#coding: utf-8
from django.shortcuts import render

from django.template import\
    Context
from django.contrib.auth.decorators import \
    login_required

from django.http import \
    HttpResponseRedirect,\
    HttpResponse, \
    Http404

from app_class.form import ClassForm, \
    Price_Tag_Form, \
    ClassPicForm, \
    ReviewForm, \
    ClassCurriForm, \
    ClassdetailForm
from app_class.models import \
    ClassPost, \
    PriceTag, \
    ClassCategory, \
    ClassPic, \
    Review, \
    ClassCurri, \
    ClassDetail

from userapp.utils import handle_uploaded_image


# Create your views here.

@login_required
def classcreate(request):
    print "class create"

    ctx = Context({
        'error':None
    })
    error = False

    if request.method=="GET":
        classform=ClassForm()
        pricetagform=Price_Tag_Form()
        class_pic_form=ClassPicForm()
        review_form=ReviewForm()
        curri_form=ClassCurriForm()
        classdetail=ClassdetailForm()

    elif request.method=="POST":
        classform=ClassForm(request.POST)
        pricetagform=Price_Tag_Form(request.POST)
        class_pic_form=ClassPicForm(request.FILES)
        review_form=ReviewForm(request.POST, request.FILES)
        curri_form=ClassCurriForm(request.POST)
        classdetail=ClassdetailForm(request.POST)


        u_categorys = request.POST.getlist(u'category')
        u_pricetag=request.POST['price_tag']
        u_pricetag=u_pricetag.replace(" ","")
        pricetags=u_pricetag.split(",")


        photos =request.FILES.getlist("class_photo")
        photo_titles=request.POST.getlist("photo_title")

        u_reviewers=request.POST.getlist('reviewer_name')
        reviewer_photos=request.FILES.getlist('reviewer_photo')
        reviews=request.POST.getlist('review')

        curri_names=request.POST.getlist('curri_name')
        curri_detail=request.POST.getlist('curri_detail')

        video_url=request.POST["video_url"]



        for photo in photos:
            if photo.content_type != 'image/png' and photo.content_type !='image/jpeg':
                class_pic_form.add_error('class_photo', u'jpeg와 png형식의 이미지만 가능합니다.')
                print "error"
                error =True


        #start make class
        if classform.is_valid() and pricetagform.is_valid() and class_pic_form.is_valid()\
                and review_form.is_valid() and curri_form.is_valid():
            category_list=[]
            for category in u_categorys:
                _category, categ_created = ClassCategory.objects.get_or_create(category_name=category)
                if categ_created:
                    _category.save()
                category_list.append(_category)

            price_tags_list=[]
            for tag in pricetags:
                _tag, tag_created = PriceTag.objects.get_or_create(price_tag=tag)
                if tag_created:
                    _tag.save()
                price_tags_list.append(_tag)

            video_url=video_url.replace(" ","")
            video_urls=video_url.split('/')
            print video_urls[-1]
            _class = classform.save(commit=False)
            _class.user = request.user
            _class.video_url=video_urls[-1]
            _class.save()
            for category in category_list:
                _class.category.add(category)
            for tag in price_tags_list:
                _class.price_tag.add(tag)
            _class.save()

            i=0
            #save photos
            for photo in photos:
                try:
                    t = handle_uploaded_image(photo, 500, 500)
                    content=t[1]
                except Exception:
                    print Exception.message
                _classpic=ClassPic(user=request.user, classpost=_class, class_photo=content, photo_title=photo_titles[i])
                _classpic.save()

                for category in category_list:
                    _classpic.category.add(category)
                _classpic.save()
                i+=1


            #save review
            i=0
            for reviewer in u_reviewers:
                try:
                    t = handle_uploaded_image(reviewer_photos[i], 100, 100)
                    content=t[1]
                except Exception:
                    print Exception.message

                _review=Review(user=request.user, classpost=_class,
                               reviewer_name=reviewer, reviewer_photo=content,review=reviews[i])
                _review.save()
                for category in category_list:
                    _review.category.add(category)
                _review.save()
                i+=1

            #save curri
            i=0
            for curri_name in curri_names:
                _curri=ClassCurri(user=request.user, classpost=_class,
                               curri_name=curri_name, curri_detail=curri_detail[i])
                _curri.save()

                for category in category_list:
                    _curri.category.add(category)
                _curri.save()
                i+=1
            _class_detail =classdetail.save(commit=False)
            _class_detail.user = request.user
            _class_detail.post = _class
            _class_detail.save()
            for category in category_list:
                    _class_detail.category.add(category)
            _class_detail.save()

            return HttpResponseRedirect('/class/{0}'.format(_class.id))

    return render(request, 'app_class/create_class.html',
        {
            'classcreateform':classform,
            'pricetagform':pricetagform,
            'classpicform':class_pic_form,
            'reviewform':review_form,
            'curriform':curri_form,
            'classdetail':classdetail,

        })

def class_detail(request, class_num):

    ctx = Context({
        'error':None
    })
    error = False

    if request.method == "GET":
        try:
            _class_post = ClassPost.objects.get(pk=class_num)
        except _class_post.DoesNotExist:
            raise Http404("post does not exist")

    return render(request, 'app_class/class_post.html',
        {
            'class_post':_class_post
        })