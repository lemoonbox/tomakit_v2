#coding: utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import \
    User
from django.http import\
    HttpResponse,\
    Http404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import\
    api_view

from DIY_tool import \
    template_match as TEMP
from app_user_v2d1.models import \
    T2Profile
from app_comminfo.models import \
    State, \
    Category
from app_demand_v2d1.forms import\
    DemandForm, \
    T2DemandCardForm,\
    T2DemandPicForm
from app_demand_v2d1.models import \
    T2ClassDemand, \
    T2DemandPic, \
    T2DemandCard
# Create your views here.

@login_required
def demand_create(request):
    demand_data={}
    HTTP_HOST=request.META["HTTP_HOST"]
    if request.method == "GET":
        demandform=DemandForm()
        imageform=T2DemandPicForm()

    elif request.method == "POST":
        imageform=""
        demand_data={
            'category':request.POST.get('category', ''),
            'state':request.POST.get('state', ''),
            'title':request.POST.get('title', ''),
            'descript':request.POST.get('descript', ''),
            'goal':request.POST.getlist('goal',''),
            'weekday':request.POST.get('weekday', ''),
            'local':request.POST.get('local', ''),
            'mobile1':request.POST.get('mobile1',''),
            'mobile2':request.POST.get('mobile2',''),
            'mobile':request.POST.get('mobile1','')+
                    request.POST.get('mobile2',''),
            'min_price':request.POST.get('min_price', ''),
            'max_price':request.POST.get('max_price', ''),
        }
        _user=User.objects.get(username=request.user)
        T2Profile.mobli_on(_user, demand_data['mobile1'],demand_data['mobile2'])

        images=request.FILES.getlist("image", "")
        _category, create=Category.objects.get_or_create(category=demand_data['category'])
        _state=State.objects.get_or_create(state=demand_data['state'])
        demand_data['user']=_user
        demand_data['category']=_category
        demand_data['state']=_state

        demandform=DemandForm(demand_data)


        if demandform.is_valid():
            _demandpost=demandform.save(commit=True)
            demand_data["demand_id"]=_demandpost.id
            demand_data["demand_post"]=_demandpost

            cardform=T2DemandCardForm(demand_data)
            _demandcard=cardform.save()
            demand_data["demand_card"]=_demandcard

            imageform=T2DemandPicForm(demand_data, request.FILES)
            imagelist=[]
            if imageform.is_valid():
                for file in images:
                    _imagelist=imageform.savefiles()

            return render(request,TEMP.DEMAND_FINISH_V2D1,{
                "HTTP_HOST":HTTP_HOST,
                'demand_data':demand_data,
            })

    return render(request, TEMP.DEMAND_CREATE_V2D1,{
        'demandform':demandform,
        'HTTP_HOST':HTTP_HOST,
        'demand_data':demand_data,
        'imageform':imageform,

    })


@login_required
def demand_modify(request, demand_num=0):
    HTTP_HOST=request.META["HTTP_HOST"]
    if request.method == "GET":
        _post=''
        demandform=DemandForm()
        imageform=T2DemandPicForm()
        try:
            _post=T2ClassDemand.objects.get(pk=demand_num)
            if _post.user != request.user:
                raise Http404(u"포스팅이 존재 하지 않습니다.")
        except ObjectDoesNotExist:
            raise Http404(u"포스팅이 존재 하지 않습니다.")

        _user=User.objects.get(username=request.user)
        _goals=_post.goal.split("#")

        demand_data={
            'category':_post.category.category,
            'state':_post.state.state,
            'title':_post.title,
            'descript':_post.descript,
            'goal':_goals,
            'weekday':_post.weekday,
            'local':_post.local,
            'mobile1':_user.t2profile_set.first().mobli1,
            'mobile2':_user.t2profile_set.first().mobli2,
            'min_price':str(_post.min_price),
            'max_price':str(_post.max_price)
        }
    elif request.method == "POST":
        imageform=""
        demand_data={
            'category':request.POST.get('category', ''),
            'state':request.POST.get('state', ''),
            'title':request.POST.get('title', ''),
            'descript':request.POST.get('descript', ''),
            'goal':request.POST.getlist('goal',''),
            'weekday':request.POST.get('weekday', ''),
            'local':request.POST.get('local', ''),
            'mobile1':request.POST.get('mobile1',''),
            'mobile2':request.POST.get('mobile2',''),
            'mobile':request.POST.get('mobile1','')+
                    request.POST.get('mobile2',''),
            'min_price':request.POST.get('min_price', ''),
            'max_price':request.POST.get('max_price', ''),
        }
        _user=User.objects.get(username=request.user)
        T2Profile.mobli_on(_user, demand_data['mobile1'],demand_data['mobile2'])

        images=request.FILES.getlist("image", "")
        _category, create=Category.objects.get_or_create(category=demand_data['category'])
        _state, create =State.objects.get_or_create(state=demand_data['state'])
        demand_data['user']=_user
        demand_data['category']=_category
        demand_data['state']=_state

        _oldpost=T2ClassDemand.objects.get(pk=demand_num)
        _oldcard=T2DemandCard.objects.get(demand_post=_oldpost)
        demandform=DemandForm(demand_data, instance=_oldpost)
        if demandform.is_valid():
            _newpost=demandform.save()
            demand_data["demand_id"]=_newpost.id
            demand_data["demand_post"]=_newpost

            cardform=T2DemandCardForm(demand_data, instance=_oldcard)
            _newcard=cardform.save()
            demand_data["demand_card"]=_newcard

            _oldpics=T2DemandPic.objects.filter(demand_post=_oldpost)
            _oldpics.delete()
            imageform=T2DemandPicForm(demand_data, request.FILES)
            imagelist=[]
            if imageform.is_valid():
                for file in images:
                    _imagelist=imageform.savefiles()
            return render(request,TEMP.MODIFY_FINISH_V2D1,{
                "HTTP_HOST":HTTP_HOST,
                'demand_data':demand_data,
            })

    return render(request, TEMP.DEMAND_MODIFY_V2D1,{
        'demandform':demandform,
        'HTTP_HOST':HTTP_HOST,
        'demand_data':demand_data,
        'imageform':imageform,
        'demand_num':demand_num,
    })


