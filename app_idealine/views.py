#coding: utf-8
from django.shortcuts import render
import itertools

# Create your views here.
from django.template import\
    Context
from django.http import \
    HttpResponseRedirect


from app_class.models import \
    ClassPost
from app_kit.models import \
    Kit_Post

#not need login
def idealine(request):

    ctx = Context({
        'error':None
    })
    error = False

    if request.method=="GET":
        _class_line=ClassPost.objects.order_by('-id')[:9]
        _kit_line=Kit_Post.objects.order_by('-id')[:9]

        itea_line=[i for i in itertools.chain(*itertools.izip_longest(
            _class_line, _kit_line)) if i is not None]

        host= request.META['HTTP_HOST']


    return render(request, 'app_idealine/idealine.html',
        {
            'lineitem':itea_line,
            'HTTP_HOST':host,
        })

def idealine_page(request, page_num=1):

    ctx = Context({
        'error':None
    })
    error = False

    if request.method=="GET":
        _class_line=ClassPost.objects.order_by('-id')[:9]
        _kit_line=Kit_Post.objects.order_by('-id')[:9]

        itea_line=[i for i in itertools.chain(*itertools.izip_longest(
            _class_line, _kit_line)) if i is not None]

        host= request.META['HTTP_HOST']


    return render(request, 'app_idealine/idealine.html',
        {
            'lineitem':itea_line,
            'HTTP_HOST':host,
        })




def categoryline(request, category):
    ctx = Context({
        'error':None
    })
    error = False

    if request.method=="GET":
        _class_catg=ClassPost.objects.filter(category__contains=category)[:9]
        _kit_catg=Kit_Post.objects.filter(category__contains=category)[:9]

        catg_line=[i for i in itertools.chain(*itertools.izip_longest(
             _class_catg, _kit_catg)) if i is not None]
        host= request.META['HTTP_HOST']


    return render(request, 'app_idealine/categoryline.html',
        {
            'catgitem':catg_line,
            'HTTP_HOST':host,
            'category':category
        })

def test(reqeust, category, kindof):

    print category
    print kindof

    return HttpResponseRedirect('/user/profile')