#coding: utf-8
from django.shortcuts import render
import itertools

# Create your views here.
from django.template import\
    Context
from django.http import \
    HttpResponseRedirect

from app_class.models import ClassPost

#not need login
def category(request, category='all', page = 1):
    ctx = Context({
        'error':None
    })
    error = False

    if request.method=="GET":
        page = int(page)

        navline_num=5
        onepage_post_num=18
        _navline_post = navline_num*onepage_post_num

        _nav_paging =int((page-1)/5)+1

        start_pos=(page-1)*onepage_post_num
        end_pos=(page)*onepage_post_num
        start_nav_pos=(_nav_paging-1)*_navline_post
        end_nav_pos=_nav_paging*_navline_post


        host= request.META['HTTP_HOST']

        if category=="all":
            _line_post = ClassPost.objects.filter(is_active=True).order_by('-id')[start_pos:end_pos]
            _nav_post=ClassPost.objects.filter(is_active=True).order_by('-id')[start_nav_pos:end_nav_pos+1]
            _nav_post_count=_nav_post.count()

        else :
            _line_post = ClassPost.objects.filter(category__category_name=category, is_active=True).order_by('-id')[start_pos:end_pos]
            _nav_post=ClassPost.objects.filter(category__category_name=category, is_active=True).order_by('-id')[start_nav_pos:end_nav_pos+1]
            _nav_post_count=_nav_post.count()



        page_start=(_nav_paging-1)*5+1
        if (_nav_post_count-1)%onepage_post_num==0:
            page_count= int((_nav_post_count-1)/onepage_post_num)
            if(_nav_post_count==1):
                page_count=1
        else:
            page_count= int((_nav_post_count-1)/onepage_post_num)+1

        page_end=page_start+page_count
        pages=[]
        for i in range(page_start, page_end):
            page_item={}
            page_item["page"]=i
            page_item["page_current"]=(i == page)
            pages.append(page_item)

        arrows=[]
        before_next_arrow={}
        before_next_arrow["nav_next"]=(_nav_post_count>_navline_post)
        before_next_arrow["next_page"]=(_nav_paging)*5+1
        arrows.append(before_next_arrow)


        before_next_arrow={}
        before_next_arrow["nav_before"]=(_nav_paging!=1)
        before_next_arrow["befor_page"]=(_nav_paging-2)*5+1
        arrows.append(before_next_arrow)



    return render(request, 'app_idealine/categoryline.html',
        {
            'catgitem':_line_post,
            'HTTP_HOST':host,
            'category':category,

            'pages':pages,
            'arrows':arrows,
        })


# def idealine(request, page = 1):
#
#     ctx = Context({
#         'error':None
#     })
#     error = False
#
#     if request.method=="GET":
#         page = int(page)
#
#         navline_num=5
#         onepage_post_num=18
#
#
#         start_pos=(page-1)*onepage_post_num
#         end_pos=(page)*onepage_post_num
#
#
#         host= request.META['HTTP_HOST']
#         _line_post = ClassPost.objects.order_by('-id')[start_pos:end_pos+1]
#         _line_post_count=_line_post.count()
#
#         arrows=[]
#         before_next_arrow={}
#         before_next_arrow["nav_next"]=(_line_post_count>onepage_post_num)
#         before_next_arrow["next_page"]=page+1
#         arrows.append(before_next_arrow)
#
#
#         before_next_arrow={}
#         before_next_arrow["nav_before"]=(page!=1)
#         before_next_arrow["befor_page"]=page-1
#         arrows.append(before_next_arrow)
#
#     return render(request, 'app_idealine/idealine.html',
#         {
#             'lineitem':_line_post,
#             'HTTP_HOST':host,
#
#             'arrows':arrows,
#         })