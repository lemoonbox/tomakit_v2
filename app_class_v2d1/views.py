#coding: utf-8
from django.shortcuts import \
    render, \
    HttpResponseRedirect
from django.contrib.auth.decorators import \
    login_required
from django.contrib.auth.models import \
    User

from DIY_tool import template_match as TEMP
from app_comminfo.models import \
    State,\
    Category
from app_class_v2d1.models import \
    T2ClassCard, \
    T2TeachClass, \
    T2TutClass, \
    T2ClassPic
from app_class_v2d1.forms import \
    T2Class_BeginForm, \
    T2TeachClassForm, \
    T2TutClassForm, \
    T2ClassPicForm, \
    T2ClassCardForm

# Create your views here.

@login_required
def class_begin(request):

    HTTP_HOST=request.META["HTTP_HOST"]
    begin_data={}
    if request.method == "GET":
        beginform=T2Class_BeginForm()

    elif request.method == "POST":
        beginform=T2Class_BeginForm(request.POST)
        _user=User.objects.get(username=request.user)
        _category, create=Category.objects.get_or_create(
            category=request.POST.get("category", ""))
        title=request.POST.get('title')
        intro_line=request.POST.get('intro_line', "")

        classtype=request.POST.get('classtype', "")
        begin_data={
            'user':_user,
            'category':_category,
            'title':request.POST.get('title', ""),
            'intro_line':request.POST.get('intro_line', ""),
            'classtype':request.POST.get('classtype', "")
        }

        if beginform.is_valid() and classtype == "tutclass":
            _tutpost=T2TutClass(user=_user, classtype=classtype,
                        title=title, intro_line=intro_line,
                        category=_category)
            _tutpost.save()
            return HttpResponseRedirect("/v2.1/class/create/tut/"+
                                        str(_tutpost.id)+"?title="+_tutpost.title)

        elif beginform.is_valid() and classtype == 'teachclass':
            _teachpost=T2TeachClass(user=_user, classtype=classtype,
                                    title=title, intro_line=intro_line,
                                    category=_category)
            _teachpost.save()
            return HttpResponseRedirect("/v2.1/class/create/teach/"+
                                        str(_teachpost.id)+"?title="+_teachpost.title)

    return render(request, TEMP.CLASS_CREATE_BEGIN_V2D1,{
        "HTTP_HOST":HTTP_HOST,
        "beginform":beginform,
        "begin_data":begin_data
    })

def create_tut(request, class_num):
    title=""
    prefill_intro=""
    prefill_addr=""
    tut_data={}

    if request.method == "GET":
        _user=User.objects.get(username=request.user)
        tutform=T2TutClassForm()
        title=request.GET.get("title")
        prefill_intro=_user.t2hostprofile_set.first().intro_self

    elif request.method == "POST":
        locality=request.POST.get("locality", "").encode("utf-8")
        area_1=request.POST.get("area_1", "").encode("utf-8")
        sublocal_1=request.POST.get("sublocal_1", "").encode("utf-8")
        sublocal_2=request.POST.get("sublocal_2", "").encode("utf-8")
        sublocal_3=request.POST.get("sublocal_4", "").encode("utf-8")
        _state, create=check_state(request)
        addr=area_1+locality+sublocal_1+sublocal_2+sublocal_3
        addr_detail=request.POST.get("addr_deatail", "").encode("utf-8")
        _user=User.objects.get(username=request.user)
        _pre_fillpost=T2TutClass.objects.get(pk=class_num)

        images=request.FILES.getlist("image", "")
        imageform=""
        tut_data={
            "user":_user,
            "category":_pre_fillpost.category,
            "title":_pre_fillpost.title,
            "intro_line":_pre_fillpost.intro_line,
            'repeat':request.POST.get("repeat"),
            'perhour':request.POST.get("perhour"),
            'weekday':request.POST.get("weekday"),
            'price':request.POST.get('price'),
            'extra_price':request.POST.get('extra_price'),
            'video':request.POST.get("video"),
            'descript':request.POST.get("descript"),
            'curri':request.POST.get("curri"),
            'notic':request.POST.get("notic"),
            'state':_state,
            'addr':addr,
            'addr_detail':addr_detail,
        }
        tutform=T2TutClassForm(tut_data, instance=_pre_fillpost)
        prefill_intro=request.POST.get("intro_self").encode("utf-8")

        if tutform.is_valid() and _pre_fillpost.user == request.user:
            _tutpost=tutform.save()
            tut_data['tut_post']=_tutpost
            tut_data['classtype']="tutclass"
            tut_data['class_id']=_tutpost.id

            _user.intro_self=prefill_intro
            _user.save()

            cardexist=T2ClassCard.objects.filter(tut_post=_tutpost).exists()
            if cardexist:
                _pre_fillcard=T2ClassCard.objects.get(tut_post=_tutpost)
                classcardform=T2ClassCardForm(tut_data, instance=_pre_fillcard)
            else:
                classcardform=T2ClassCardForm(tut_data)
            _classcard=classcardform.save()
            tut_data['class_card']=_classcard

            image_exist=T2ClassPic.objects.filter(tut_post=_tutpost).exists()
            if image_exist:
                _old_images=T2ClassPic.objects.filter(tut_post=_tutpost)
                _old_images.delete()
            imageform=T2ClassPicForm(tut_data, request.FILES)
            imagelist=[]
            if imageform.is_valid():
                _imagelist=imageform.savefiles()

            return render(request, TEMP.CLASS_CREATE_FINISH_V2D1,{
                    })

    return render(request, TEMP.CLASS_CREATE_TUT_V2D1,{
        "tutform":tutform,
        "title":title,
        ''
        "class_num":class_num,
        "prefill_intro":prefill_intro,
        "tut_data":tut_data,
        "imageform":imageform,
        #"prefill_addr":prefill_addr
    })

@login_required
def create_teach(request, class_num):
    title=""
    prefill_intro=""
    prefill_addr=""
    teach_data={}
    if request.method == "GET":
        _user=User.objects.get(username=request.user)
        teachform=T2TeachClassForm()
        title=request.GET.get("title")
        prefill_intro=_user.t2hostprofile_set.first().intro_self
        #prefill_addr=_user.t2hostprofile_set.first().shop_addr
    elif request.method == "POST":
        locality=request.POST.get("locality", "").encode("utf-8")
        area_1=request.POST.get("area_1", "").encode("utf-8")
        sublocal_1=request.POST.get("sublocal_1", "").encode("utf-8")
        sublocal_2=request.POST.get("sublocal_2", "").encode("utf-8")
        sublocal_3=request.POST.get("sublocal_4", "").encode("utf-8")
        _state, create=check_state(request)
        addr=area_1+locality+sublocal_1+sublocal_2+sublocal_3
        addr_detail=request.POST.get("addr_deatail", "").encode("utf-8")
        _user=User.objects.get(username=request.user)
        _pre_fillpost=T2TeachClass.objects.get(pk=class_num)

        images=request.FILES.getlist("image", "")
        imageform=""
        teach_data={
            "user":_user,
            "category":_pre_fillpost.category,
            "title":_pre_fillpost.title,
            "intro_line":_pre_fillpost.intro_line,
            'repeat':request.POST.get("repeat"),
            'perhour':request.POST.get("perhour"),
            'weekday':request.POST.get("weekday"),
            'max_num':request.POST.get("max_num"),
            "min_num":request.POST.get('min_num'),
            'startday':request.POST.get('startday'),
            'deadline':request.POST.get('deadline'),
            'price':request.POST.get('price'),
            'extra_price':request.POST.get('extra_price'),
            'video':request.POST.get("video"),
            'descript':request.POST.get("descript"),
            'curri':request.POST.get("curri"),
            'notic':request.POST.get("notic"),
            'state':_state,
            'addr':addr,
            'addr_detail':addr_detail,
        }
        teachform=T2TeachClassForm(teach_data, instance=_pre_fillpost)
        prefill_intro=request.POST.get("intro_self").encode("utf-8")

        if teachform.is_valid() and _pre_fillpost.user == request.user:
            _teachpost=teachform.save()
            teach_data['teach_post']=_teachpost
            teach_data['classtype']="teachclass"
            teach_data['class_id']=_teachpost.id

            _user.intro_self=prefill_intro
            _user.save()

            cardexist=T2ClassCard.objects.filter(teach_post=_teachpost).exists()
            if cardexist:
                _pre_fillcard=T2ClassCard.objects.get(teach_post=_teachpost)
                classcardform=T2ClassCardForm(teach_data, instance=_pre_fillcard)
            else:
                classcardform=T2ClassCardForm(teach_data)
            _classcard=classcardform.save()
            teach_data['class_card']=_classcard

            image_exist=T2ClassPic.objects.filter(teach_post=_teachpost).exists()
            if image_exist:
                _old_images=T2ClassPic.objects.filter(teach_post=_teachpost)
                _old_images.delete()
            imageform=T2ClassPicForm(teach_data, request.FILES)
            imagelist=[]
            if imageform.is_valid():
                _imagelist=imageform.savefiles()

            return render(request, TEMP.CLASS_CREATE_FINISH_V2D1,{
            })

    return render(request, TEMP.CLASS_CREATE_TEACH_V2D1,{
        "teachform":teachform,
        "title":title,
        "class_num":class_num,
        "prefill_intro":prefill_intro,
        "teach_data":teach_data,
        "imageform":imageform,
        #"prefill_addr":prefill_addr
    })


def check_state(request):

    if request:
        locality=request.POST.get("locality", "")
        area_1=request.POST.get("area_1", "")

        local_list=[locality.encode("utf-8"), area_1.encode("utf-8")]

        for local in local_list:
            if local in ["서울특별시"]:
                _state=State.objects.get_or_create(state="seoul")
                return _state
            elif local in ["인천광역시", "경기도"]:
                _state=State.objects.get_or_create(state="incheon_gyeonggi")
                return _state
            elif local in ['부산광역시','울산광역시','경상남도']:
                _state=State.objects.get_or_create(state="busan_ulsan_gyeongnam")
                return _state
            elif local in ['대구광역시', '경상북도']:
                _state=State.objects.get_or_create(state="daegu_gyeongbuk")
                return _state
            elif local in ['대전광역시','세종특별자치시', '충청북도', '충청남도']:
                _state=State.objects.get_or_create(state="daejeon_chungcheong")
                return _state
            elif local in ['광주광역시', '전라북도', '전라남도']:
                _state=State.objects.get_or_create(state="gwangju_jeonla")
                return _state
            elif local in ['강원도']:
                _state=State.objects.get_or_create(state="gangwon")
                return _state
            elif local in ['제주특별자치도']:
                _state=State.objects.get_or_create(state="jeju")
                return _state
        _state=State.objects.get_or_create(state="etc")
        return _state
    else :
        return False