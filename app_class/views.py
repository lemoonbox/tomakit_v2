#coding: utf-8
from django.shortcuts import render

from django.template import\
    Context
from django.contrib.auth.decorators import \
    login_required

from app_class.form import ClassForm, Price_Tag_Form, ClassPicForm, ReviewForm
from app_class.models import ClassPost, PriceTag, ClassCategory, ClassPic

from userapp.utils import handle_uploaded_image


# Create your views here.

@login_required
def classcreate(request):

    ctx = Context({
        'error':None
    })
    error = False

    if request.method=="GET":
        classform=ClassForm()
        pricetagform=Price_Tag_Form()
        class_pic_form=ClassPicForm()
        review_form=ReviewForm()

    elif request.method=="POST":
        classform=ClassForm(request.POST)
        pricetagform=Price_Tag_Form(request.POST)
        class_pic_form=ClassPicForm(request.FILES)
        review_form=ReviewForm(request.POST, request.FILES)

        u_categorys = request.POST.getlist(u'category')
        u_pricetag=request.POST['price_tag']
        u_pricetag=u_pricetag.replace(" ","")
        pricetags=u_pricetag.split(",")


        photos =request.FILES.getlist("class_photo")

        u_reviewers=request.POST.getlist('reviewer_name')
        reviewer_photos=request.POST.getlist('reviewer_photo')
        reviews=request.POST.getlist('review')

        print u_reviewers
        print reviewer_photos
        print reviews

        for photo in photos:
            if photo.content_type != 'image/png' and photo.content_type !='image/jpeg':
                class_pic_form.add_error('class_photo', u'jpeg와 png형식의 이미지만 가능합니다.')
                print "error"
                error =True


        #start make class
        if classform.is_valid() and pricetagform.is_valid():
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

            _class = classform.save(commit=False)
            _class.user = request.user
            _class.save()
            for category in category_list:
                _class.category.add(category)
            for tag in price_tags_list:
                _class.price_tag.add(tag)
            _class.save()

            for photo in photos:
                try:
                    t = handle_uploaded_image(photo, 500, 500)
                    content=t[1]
                except Exception:
                    print Exception.message
                _classpic=ClassPic(user=request.user, classpost=_class, class_photo=content)
                _classpic.save()

                for category in category_list:
                    _classpic.category.add(category)
                _classpic.save()



    return render(request, 'app_class/create_class_dev_moon.html',
        {
            'classcreateform':classform,
            'pricetagform':pricetagform,
            'classpicform':class_pic_form,
            'reviewform':review_form,

        })