#coding:utf-8
from django.shortcuts import render

from app_board.models import Questionbox, SolutionBox, Casebox, MainQoubox
from app_comminfo.models import State, Category
from DIY_tool import template_match as TEMP
# Create your views here.


def questionboard(request, page=1, category = 'all', state='all'):

    if request.method == "GET":

        cate_condt =[]
        state_condt=[]
        _categories = Category.objects.all()
        _states = State.objects.all()

        if category == 'all':
            for _cate in _categories:
                cate_condt.append(_cate.category)
        else :
            cate_condt.append(category)

        if state == 'all':
            for _state in _states:
                state_condt.append(_state.state)
        else :
            state_condt.append(state)


        paging_date = pagination(navline_num=2, onepage_post_num=15,
                                 target_model=Questionbox, cate_condt=cate_condt, state_condt =state_condt, page=page)

        HTTP_HOST = request.META['HTTP_HOST']
        _questions = paging_date['pageitme']
        arrows = paging_date['arrows']
        pages = paging_date['pages']
        categories = paging_date['categories']
        states = paging_date['states']
    else:
        pass

    return render(request, TEMP.V2_BOARD_QUESTION,{
        'questions':_questions,

        'categoryies':categories,
        'states':states,

        "page_currunt":page,
        "cate_current":category,
        "state_current":state,

        'arrows' : arrows,
        'pages':pages,
        'HTTP_HOST':HTTP_HOST,
    })


def caseboard(request,page=1, category = 'all', state='all'):

    if request.method == "GET":
        cate_condt =[]
        state_condt=[]
        _categories = Category.objects.all()
        _states = State.objects.all()

        if category == 'all':
            for _cate in _categories:
                cate_condt.append(_cate.category)
        else :
            cate_condt.append(category)

        if state == 'all':
            for _state in _states:
                state_condt.append(_state.state)
        else :
            state_condt.append(state)


        paging_date = pagination(navline_num=2, onepage_post_num=8,
                                 target_model=Casebox, cate_condt=cate_condt, state_condt =state_condt, page=page)

        HTTP_HOST = request.META['HTTP_HOST']
        _case = paging_date['pageitme']
        arrows = paging_date['arrows']
        pages = paging_date['pages']
        categories = paging_date['categories']
        states = paging_date['states']

    else:
        pass

    return render(request, TEMP.V2_BOARD_CASE,{
        'questions':_case,

        'categoryies':categories,
        'states':states,

        "page_currunt":page,
        "cate_current":category,
        "state_current":state,

        'arrows' : arrows,
        'pages':pages,
        'HTTP_HOST':HTTP_HOST,
    })



def pagination(navline_num=5, onepage_post_num=20,target_model=None,
               cate_condt=[], state_condt=[], page = 1):

    from app_board.models import Questionbox, Casebox




    if not target_model:
        raise ImportError("This function need model")

    page = int(page)


    navline_num=navline_num
    onepage_post_num=onepage_post_num
    _navline_post = navline_num*onepage_post_num

    _nav_paging =int((page-1)/navline_num)+1

    start_pos=(page-1)*onepage_post_num
    end_pos=(page)*onepage_post_num
    start_nav_pos=(_nav_paging-1)*_navline_post
    end_nav_pos=_nav_paging*_navline_post



    if target_model is Questionbox :
        _line_post = target_model.objects.filter(category__category__in  = cate_condt,
                                                 state__state__in = state_condt, is_active=True,
                                                 is_solved=False).order_by('-id')[start_pos:end_pos]
        _nav_post=target_model.objects.filter(category__category__in  = cate_condt,
                                                 state__state__in = state_condt, is_active=True,
                                                 is_solved=False).order_by('-id')[start_nav_pos:end_nav_pos+1]
        _nav_post_count=_nav_post.count()

    else:
        _line_post = target_model.objects.filter(category__category__in  = cate_condt,
                                                 state__state__in = state_condt, is_active=True,).order_by('-id')[start_pos:end_pos]
        _nav_post=target_model.objects.filter(category__category__in  = cate_condt,
                                                 state__state__in = state_condt, is_active=True,).order_by('-id')[start_nav_pos:end_nav_pos+1]
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


    #category list and now active
    #cate_condt[0] is always leather
    categoris=[]



    for cate in Category.objects.all():
        cate_item={}
        cate_item["category"]=str(cate.category)
        cate_item["category_current"]=(True if len(cate_condt)==1 and str(cate)==cate_condt[0] else False)
        cate_item["state"]=("all" if len(state_condt)>=2 else str(state_condt[0]))
        categoris.append(cate_item)


    cate_item={}
    cate_item["category"]="all"
    cate_item["category_current"]=(True if len(cate_condt)>=2 else False)
    cate_item["state"]=("all" if len(state_condt)>=2 else str(state_condt[0]))
    categoris.append(cate_item)

    #state list and now active
    states = []

    for state in State.objects.all():
        state_item={}
        state_item["state"]=str(state.state)
        state_item["state_current"]=(True if len(state_condt)==1 and str(state)==state_condt[0] else False)
        state_item["category"]=("all" if len(cate_condt)>=2 else str(cate_condt[0]))
        states.append(state_item)

    state_item={}
    state_item["state"]="all"
    state_item["state_current"]=(True if len(state_condt)>=2 else False)
    state_item["category"]=("all" if len(cate_condt)>=2 else str(cate_condt[0]))
    states.append(state_item)


    return {'pageitme':_line_post, 'pages':pages, 'arrows':arrows,
            'categories':categoris, 'states':states}


def mainboard(request):


    if request.method=="GET":
        _mainqouboxs=MainQoubox.objects.all()[0:5]
        HTTP_HOST= request.META['HTTP_HOST']



    return render(request, 'contents/main/categoryline.html',
        {
            'qouboxs':_mainqouboxs,
            'HTTP_HOST':HTTP_HOST,

            'next':"/",
        })