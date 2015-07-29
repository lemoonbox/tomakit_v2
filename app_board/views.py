from django.shortcuts import render

from app_board.models import Questionbox, SolutionBox, Casebox
from DIY_tool import template_match as TEMP
# Create your views here.


def questionboard(request, page=1):

    if request.method == "GET":

        paging_date = pagination(navline_num=2, onepage_post_num=2, target_model=Questionbox, category='all', page=page)

        HTTP_HOST = request.META['HTTP_HOST']
        _questions = paging_date['pageitme']
        arrows = paging_date['arrows']
        pages = paging_date['pages']
    else:
        pass

    return render(request, TEMP.V2_BOARD_QUESTION,{
        'questions':_questions,

        'arrows' : arrows,
        'pages':pages,
        'HTTP_HOST':HTTP_HOST,
    })


def caseboard(request,page=1):

    if request.method == "GET":
        paging_date = pagination(navline_num=2, onepage_post_num=2, target_model=Casebox, category='all', page=page)

        HTTP_HOST = request.META['HTTP_HOST']
        _questions = paging_date['pageitme']
        arrows = paging_date['arrows']
        pages = paging_date['pages']

    else:
        pass

    return render(request, TEMP.V2_BOARD_CASE,{
        'questions':_questions,

        'arrows' : arrows,
        'pages':pages,
        'HTTP_HOST':HTTP_HOST,
    })



def pagination(navline_num=5, onepage_post_num=20,target_model=None, category='all', page = 1):

    if not target_model:
        raise ImportError("This function need model")

    page = int(page)
    print navline_num
    print onepage_post_num
    print page

    navline_num=navline_num
    onepage_post_num=onepage_post_num
    _navline_post = navline_num*onepage_post_num

    _nav_paging =int((page-1)/navline_num)+1

    start_pos=(page-1)*onepage_post_num
    end_pos=(page)*onepage_post_num
    start_nav_pos=(_nav_paging-1)*_navline_post
    end_nav_pos=_nav_paging*_navline_post

    if category=="all":
        _line_post = target_model.objects.filter(is_active=True).order_by('-id')[start_pos:end_pos]
        _nav_post=target_model.objects.filter(is_active=True).order_by('-id')[start_nav_pos:end_nav_pos+1]
        _nav_post_count=_nav_post.count()

    else :
        _line_post = target_model.objects.filter(category__category_name=category, is_active=True).order_by('-id')[start_pos:end_pos]
        _nav_post=target_model.objects.filter(category__category_name=category, is_active=True).order_by('-id')[start_nav_pos:end_nav_pos+1]
        _nav_post_count=_nav_post.count()



    page_start=(_nav_paging-1)*navline_num+1
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
    before_next_arrow["next_page"]=(_nav_paging)*navline_num+1
    arrows.append(before_next_arrow)


    before_next_arrow={}
    before_next_arrow["nav_before"]=(_nav_paging!=1)
    before_next_arrow["befor_page"]=(_nav_paging-2)*navline_num+1
    arrows.append(before_next_arrow)



    return {'pageitme':_line_post, 'pages':pages, 'arrows':arrows}
