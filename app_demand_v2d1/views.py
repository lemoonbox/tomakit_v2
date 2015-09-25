#coding: utf-8
from django.shortcuts import render, \
    get_object_or_404
from django.contrib.auth.decorators import \
    login_required,\
    user_passes_test
from django.contrib.auth.models import \
    User
from django.http import\
    HttpResponse,\
    Http404,\
    HttpResponseRedirect
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
    T2DemandPicForm,\
    CommentForm, \
    MobliForm
from app_demand_v2d1.models import \
    T2ClassDemand, \
    T2DemandPic, \
    T2DemandCard, \
    T2DemandCmt
# Create your views here.
def profile_check(user):
    if user.t2profile_set.first():
        return True
    else :
        return False

@login_required
@user_passes_test(profile_check, login_url="/v2.1/user/host/apply/")
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
        print "images"
        print images
        _category, create=Category.objects.get_or_create(category=demand_data['category'])
        _state, create=State.objects.get_or_create(state=demand_data['state'])
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
@user_passes_test(profile_check, login_url="/v2.1/user/host/apply/")
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

def demand_detail(request, demand_num):
    HTTP_HOST=request.META["HTTP_HOST"]
    if request.method == "GET":
        exist=T2ClassDemand.objects.filter(pk=demand_num).exists()

        if exist:
            _post=T2ClassDemand.objects.filter(pk=demand_num)[0]

            return render(request, TEMP.DEMAND_DETAIL_V2D1,{
                "post":_post,
                "HTTP_HOST":HTTP_HOST,
            })

        else:

            raise Http404("개시물이 존재 하지 않습니다.")
    else :
        raise Http404("잘못된 요청 입니다.")


def create_comment(request, demand_num):

    if request.method == "POST":
        _post=T2ClassDemand.objects.get(pk=demand_num)
        class_ad=request.POST.get("class_ad", "")
        if class_ad:
            class_ad=True
        else:
            class_ad=False
        _user=User.objects.get(username=request.user)
        commnet=request.POST.get("comment")
        commentform=CommentForm(request.POST)

        if commentform.is_valid():
            _comment=T2DemandCmt(user=_user, demand_post=_post,
                                 comment=commnet, class_ad=class_ad)
            _comment.save()
        return HttpResponseRedirect("/v2.1/demand/%d" %(_post.id))
    else:
        return Http404("잘못된 요청입니다.")

def modify_comment(request, demand_num):

    if request.method == "POST":
        class_ad=False
        _post=T2ClassDemand.objects.get(pk=demand_num)
        class_ad=request.POST.get("class_ad", "")
        comment_id=request.POST.get('comment_num', "")
        if class_ad:
            class_ad=True
        _user=User.objects.get(username=request.user)
        comment=request.POST.get("comment", "")
        commentform=CommentForm(request.POST)
        _comment=T2DemandCmt.objects.get(pk=comment_id)
        if commentform.is_valid() and _user == _comment.user:
            _comment.comment=comment
            _comment.class_ad=class_ad
            _comment.save()
        return HttpResponseRedirect("/v2.1/demand/%d" %(_post.id))
    else:
        return Http404("잘못된 요청입니다.")


def delete_comment(request, comment_num):

    if request.method == "POST":
        _comment=T2DemandCmt.objects.get(pk=comment_num)
        post_id=request.POST.get("demand_num", "")
        _post=T2ClassDemand.objects.get(pk=post_id)

        if _comment.user == request.user:
            _comment.is_active=False
            _comment.save()

        return HttpResponseRedirect("/v2.1/demand/%d" %(_post.id))

    else:
        return  Http404("잘못된 요청입니다.")

@login_required
@user_passes_test(profile_check, login_url="/v2.1/user/host/apply/")
def mobli_required(request, post_num):
    HTTP_HOST=request.META["HTTP_HOST"]
    if request.method == "GET":
        mobliform=MobliForm()
        lineup_next=request.GET.get("lineup_next", "/")

    elif request.method == "POST":
        lineup_next=request.POST.get("lineup_next", "/")
        mobli1=request.POST.get('mobli1', "")
        mobli2=request.POST.get('mobli2', "")
        mobli="010"+mobli1+mobli2

        _user=User.objects.get(username=request.user)

        _profile=_user.t2profile_set.first()
        _profile.mobli=mobli
        _profile.mobli_able=True
        _profile.save()

        return HttpResponseRedirect("/v2.1/demand/lineup/"+post_num+"?lineup_next="+lineup_next)

    return render(request, TEMP.LINEUP_REQUIRE_V2D1,{
        "HTTP_HOST":HTTP_HOST,
        "mobliform":mobliform,
        "lineup_next":lineup_next,
        "post_num":post_num,

    })



@login_required
def lineup_demand(request, demand_num, page=1,category=all, state=all):

    lineup_next=request.GET.get("lineup_next", "/")
    _demand_post= get_object_or_404(T2ClassDemand, pk=demand_num)
    _demand_card=get_object_or_404(T2DemandCard, pk=demand_num)

    if T2ClassDemand.objects.filter(
        id=_demand_post.id, inline_users__in=[request.user,]).exists():
        _demand_post.inline_users.remove(request.user)
        _demand_card.inline_users.remove(request.user)

    else:
        _demand_post.inline_users.add(request.user)
        _demand_card.inline_users.add(request.user)

    return HttpResponseRedirect(lineup_next)



