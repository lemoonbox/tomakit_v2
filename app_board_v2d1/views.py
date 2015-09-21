from django.shortcuts import render
from DIY_tool import template_match as TEMP
from django.http import\
    HttpResponseRedirect

from app_comminfo.models import \
    State, \
    Category
from app_board_v2d1.models import Bestclass
from app_class_v2d1.models import T2ClassCard
from app_demand_v2d1.models import T2DemandCard

# Create your views here.


def mainpage(request):
    next="/"
    HTTP_HOST = request.META['HTTP_HOST']
    if request.method == "GET":
        adkeyword=request.GET.get("keyword", "all")
        _bestlist=[]
        if adkeyword == "all":
            _bestlist=Bestclass.objects.filter(is_active=True).order_by('-id')[0:3]
        else:
            _bestlist=Bestclass.objects.filter(keyword=adkeyword, is_active=True).order_by('-id')[0:3]

    elif request.method == "POST":
        pass
    return render(request, TEMP.INDEX_PAGE_V2D1,{
        'bestlist':_bestlist,
        "HTTP_HOST":HTTP_HOST,
        "next":next,
    })

def class_filter_redirect(request):
    _category=""
    _state=""
    print request.GET
    if request.method == "GET":
        _category=request.GET.get("category", "all")
        print _category
        _state=request.GET.get("state", "all")
        print _state
    else:
        pass

    return HttpResponseRedirect("/v2.1/board/class_list/1/"+_category+"/"+_state)


def class_list_board(request, page=1, category = 'all', state='all'):

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


        paging_date = pagination(navline_num=5, onepage_post_num=6,
                                 target_model=T2ClassCard, cate_condt=cate_condt,
                                 state_condt =state_condt, page=page)

        HTTP_HOST = request.META['HTTP_HOST']
        _regul_class = paging_date['pageitme']
        arrows = paging_date['arrows']
        pages = paging_date['pages']
        categories = paging_date['categories']
        states = paging_date['states']

    else:
        pass
    next ="/v2.1/index/demandlist"
    return render(request, TEMP.REGUL_CLASS_LIST_V2D1,{
        'classlist':_regul_class,

        'categoryies':categories,
        'states':states,

        "page_currunt":page,
        "cate_current":category,
        "state_current":state,

        'arrows' : arrows,
        'pages':pages,
        'HTTP_HOST':HTTP_HOST,
        'next':next,
    })

def demand_list_board(request, page=1, category = 'all', state='all'):
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


        paging_date = pagination(navline_num=2, onepage_post_num=1,
                                 target_model=T2DemandCard, cate_condt=cate_condt,
                                 state_condt =state_condt, page=page)

        HTTP_HOST = request.META['HTTP_HOST']
        _regul_class = paging_date['pageitme']
        arrows = paging_date['arrows']
        pages = paging_date['pages']
        categories = paging_date['categories']
        states = paging_date['states']

    else:
        pass
    next ="/v2.1/board/demand_list"
    return render(request, TEMP.DEMAND_LIST_V2D1,{
        'classlist':_regul_class,

        'categoryies':categories,
        'states':states,

        "page_currunt":page,
        "cate_current":category,
        "state_current":state,

        'arrows' : arrows,
        'pages':pages,
        'HTTP_HOST':HTTP_HOST,
        'next':next,
    })

def demand_filter_redirect(request):
    _category=""
    _state=""
    print request.GET
    if request.method == "GET":
        _category=request.GET.get("category", "all")
        print _category
        _state=request.GET.get("state", "all")
        print _state
    else:
        pass

    return HttpResponseRedirect("/v2.1/board/demand_list/1/"+_category+"/"+_state)

def pagination(navline_num=5, onepage_post_num=20,target_model=None,
               cate_condt=[], state_condt=[], page = 1):

    from app_board_v2d1.models import T2ClassCard
    from app_demand_v2d1.models import T2DemandCard


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



    if target_model is T2ClassCard :
        _line_post = target_model.objects.filter(
            category__category__in  = cate_condt,state__state__in = state_condt,
            is_active=True, is_open=True).order_by('pop_point')[start_pos:end_pos]
        _nav_post=target_model.objects.filter(
            category__category__in  = cate_condt, state__state__in = state_condt,
            is_active=True, is_open=True).order_by('pop_point')[start_nav_pos:end_nav_pos+1]
        _nav_post_count=_nav_post.count()

    else:
        _line_post = target_model.objects.filter(
            category__category__in  = cate_condt,state__state__in = state_condt,
            is_active=True,).order_by('-id')[start_pos:end_pos]
        _nav_post=target_model.objects.filter(
            category__category__in  = cate_condt,state__state__in = state_condt,
            is_active=True,).order_by('-id')[start_nav_pos:end_nav_pos+1]
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
    categoris.insert(0,cate_item)

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
    states.insert(0,state_item)


    return {'pageitme':_line_post, 'pages':pages, 'arrows':arrows,
            'categories':categoris, 'states':states}