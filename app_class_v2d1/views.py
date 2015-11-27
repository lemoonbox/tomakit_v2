#coding: utf-8
from PIL import Image
from StringIO import StringIO
import requests, base64

from django.shortcuts import \
    render, \
    HttpResponseRedirect
from django.contrib.auth.decorators import \
    login_required, \
    permission_required,\
    user_passes_test
from django.contrib.auth.models import \
    User
from django.core.exceptions import \
    ObjectDoesNotExist
from django.http import \
    Http404
from django.shortcuts import render, \
    get_object_or_404
import  datetime
from django.core.files.uploadedfile import\
    InMemoryUploadedFile


from DIY_tool import template_match as TEMP
from app_comminfo.models import \
    State,\
    Category
from app_class_v2d1.models import \
    T2ClassCard, \
    T2TeachClass, \
    T2TutClass, \
    T2ClassPic, \
    T2ClassReview, \
    T2CardPic
from app_class_v2d1.forms import \
    T2Class_BeginForm, \
    T2TeachClassForm, \
    T2TutClassForm, \
    T2ClassPicForm, \
    T2ClassCardForm,\
    T2ReviewForm, \
    T2CardPicForm
from app_user_v2d1.models import \
    T2HostProfile
from DIY_tool.settings import LOCAL

from utils.utils import shard_url_picker


# Create your views here.
def host_check(user):
    if user.t2hostprofile_set.first() or user.is_staff:
        return True
    else :
        return False


@login_required
@user_passes_test(host_check, login_url="/v2.1/user/host/apply/")
def class_begin(request):

    HTTP_HOST=request.META["HTTP_HOST"]
    begin_data={}
    if request.method == "GET":
        beginform=T2Class_BeginForm()
        _user=User.objects.get(username=request.user)

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
        print request.POST.get("category","")

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

@login_required
@user_passes_test(host_check, login_url="/v2.1/user/host/apply/")
def create_tut(request, class_num):
    title=""
    prefill_intro=""
    prefill_addr=""
    tut_data={}
    HTTP_HOST=request.META["HTTP_HOST"]

    if request.method == "GET":
        _user=User.objects.get(username=request.user)
        tutform=T2TutClassForm()
        title=request.GET.get("title")
        prefill_intro=_user.t2hostprofile_set.first().intro_self

        imageform=T2ClassPicForm()


    elif request.method == "POST":
        locality=request.POST.get("locality", "").encode("utf-8")
        area_1=request.POST.get("area_1", "").encode("utf-8")
        sublocal_1=request.POST.get("sublocal_1", "").encode("utf-8")
        sublocal_2=request.POST.get("sublocal_2", "").encode("utf-8")
        sublocal_4=request.POST.get("sublocal_4", "").encode("utf-8")
        _state, create=check_state(request)
        addr=area_1+" "+locality+" "+sublocal_1+" "+sublocal_2+" "+sublocal_4
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
            'locality':locality,
            'area_1':area_1,
            'sublocal_1': sublocal_1,
            'sublocal_2': sublocal_2,
            'sublocal_4': sublocal_4,
            'addr':addr,
            'addr_detail':addr_detail,
        }
        tutform=T2TutClassForm(tut_data, instance=_pre_fillpost)
        imageform=T2ClassPicForm(tut_data, request.FILES)
        prefill_intro=request.POST.get("intro_self").encode("utf-8")

        if tutform.is_valid() and imageform.is_valid() and \
                        _pre_fillpost.user == request.user:
            _tutpost=tutform.save()
            tut_data['tut_post']=_tutpost
            tut_data['classtype']="tutclass"
            tut_data['class_id']=_tutpost.id

            _user.intro_self=prefill_intro
            _user.save()

            _classcard_set=T2ClassCard.objects.filter(tut_post=_tutpost)
            if _classcard_set.exists():
                classcardform=T2ClassCardForm(tut_data, instance=_classcard_set[0])
            else:
                classcardform=T2ClassCardForm(tut_data)
            _classcard=classcardform.save()
            tut_data['class_card']=_classcard

            _class_image=T2ClassPic.objects.filter(tut_post=_tutpost)
            _card_image=T2CardPic.objects.filter(class_card=_classcard)
            if _class_image.exists():
                _class_image.delete()
                _card_image.delete()

            imagelist=[]
            request.FILES["card_img"]=request.FILES.getlist("image", "")[0]
            card_imageform=T2CardPicForm(tut_data, request.FILES)
            if imageform.is_valid():
                _imagelist=imageform.savefiles()
                _card_image=card_imageform.save_img()

            _hostprofile=T2HostProfile.objects.get(user=_user)
            _hostprofile.intro_self=request.POST.get("intro_self", "")
            _hostprofile.save()
            _tutpost.wr_done=True
            _classcard.wr_done=True
            _tutpost.is_open=True
            _classcard.is_open=True
            _tutpost.save()
            _classcard.save()
            return render(request, TEMP.CLASS_CREATE_FINISH_V2D1,{
                        "HTTP_HOST":HTTP_HOST,
                        "cl_card_id":_classcard.id,
                        'user':_user,
                    })

    return render(request, TEMP.CLASS_CREATE_TUT_V2D1,{
        "tutform":tutform,
        "title":title,
        "class_num":class_num,
        "prefill_intro":prefill_intro,
        "tut_data":tut_data,
        "imageform":imageform,
        "HTTP_HOST":HTTP_HOST,
        #"prefill_addr":prefill_addr
    })

@login_required
@user_passes_test(host_check, login_url="/v2.1/user/host/apply/")
def create_teach(request, class_num):
    title=""
    prefill_intro=""
    prefill_addr=""
    teach_data={}
    HTTP_HOST=request.META["HTTP_HOST"]
    if request.method == "GET":
        _user=User.objects.get(username=request.user)
        teachform=T2TeachClassForm()
        title=request.GET.get("title")
        prefill_intro=_user.t2hostprofile_set.first().intro_self
        imageform=T2ClassPicForm()
    elif request.method == "POST":
        locality=request.POST.get("locality", "").encode("utf-8")
        area_1=request.POST.get("area_1", "").encode("utf-8")
        sublocal_1=request.POST.get("sublocal_1", "").encode("utf-8")
        sublocal_2=request.POST.get("sublocal_2", "").encode("utf-8")
        sublocal_4=request.POST.get("sublocal_4", "").encode("utf-8")
        _state, create=check_state(request)
        addr=area_1+" "+locality+" "+sublocal_1+" "+sublocal_2+" "+sublocal_4
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
            'locality':locality,
            'area_1':area_1,
            'sublocal_1': sublocal_1,
            'sublocal_2': sublocal_2,
            'sublocal_4': sublocal_4,
            'addr':addr,
            'addr_detail':addr_detail,
        }
        teachform=T2TeachClassForm(teach_data, instance=_pre_fillpost)
        imageform=T2ClassPicForm(teach_data, request.FILES)
        prefill_intro=request.POST.get("intro_self").encode("utf-8")

        if teachform.is_valid() and imageform.is_valid()\
                and _pre_fillpost.user == request.user:
            _teachpost=teachform.save()
            teach_data['teach_post']=_teachpost
            teach_data['classtype']="teachclass"
            teach_data['class_id']=_teachpost.id

            _user.intro_self=prefill_intro
            _user.save()

            _calsscard_set=T2ClassCard.objects.filter(teach_post=_teachpost)
            if _calsscard_set.exists():
                classcardform=T2ClassCardForm(teach_data, instance=_calsscard_set[0])
            else:
                classcardform=T2ClassCardForm(teach_data)
            _classcard=classcardform.save()
            teach_data['class_card']=_classcard

            _class_image=T2ClassPic.objects.filter(teach_post=_teachpost)
            _card_image=T2CardPic.objects.filter(class_card=_classcard)
            if _class_image.exists():
                _class_image.delete()
                _card_image.delete()

            imagelist=[]
            request.FILES["card_img"]=request.FILES.getlist("image", "")[0]
            card_imageform=T2CardPicForm(teach_data, request.FILES)
            if imageform.is_valid():
                _imagelist=imageform.savefiles()
                _card_image=card_imageform.save_img()

            _hostprofile=T2HostProfile.objects.get(user=_user)
            _hostprofile.intro_self=request.POST.get("intro_self", "")
            _hostprofile.save()
            _teachpost.wr_done=True
            _classcard.wr_done=True
            _teachpost.is_open=True
            _classcard.is_open=True
            _teachpost.save()
            _classcard.save()
            return render(request, TEMP.CLASS_MODIFY_FINISH_V2D1,{
                "HTTP_HOST":HTTP_HOST,
                "cl_card_id":_classcard.id,
                'user':_user
            })

    return render(request, TEMP.CLASS_CREATE_TEACH_V2D1,{
        "teachform":teachform,
        "title":title,
        "class_num":class_num,
        "prefill_intro":prefill_intro,
        "teach_data":teach_data,
        "imageform":imageform,
        "HTTP_HOST":HTTP_HOST,
        #"prefill_addr":prefill_addr
    })

@login_required
@user_passes_test(host_check, login_url="/v2.1/user/host/apply/")
def modify_teach(request, class_num):
    HTTP_HOST=request.META["HTTP_HOST"]
    if request.method == "GET":
        teachform=T2TeachClassForm()
        imageform=T2ClassPicForm()
        try :
            _post=T2TeachClass.objects.get(pk=class_num)
            if _post.user != request.user and not request.user.is_staff:
                raise Http404("수정 가능한 사용자가 아닙니다.")
        except ObjectDoesNotExist:
            raise Http404("포스팅이 존재 하지 않습니다.")

        _user=User.objects.get(username=request.user)
        teach_data={
            "user":_user,
            "post":_post,
            "category":_post.category,
            "title":_post.title,
            "intro_line":_post.intro_line,
            "classtype":_post.classtype,
            'repeat':int(_post.repeat),
            'perhour':int(_post.perhour),
            'weekday':_post.weekday,
            'max_num':str(_post.max_num),
            "min_num":str(_post.min_num),
            'startday':_post.startday,
            'deadline':_post.deadline,
            'price':str(_post.price),
            'extra_price':str(_post.extra_price),
            'video':_post.video,
            'descript':_post.descript,
            'curri':_post.curri,
            'notic':_post.notic,
            'state':_post.state,
            'locality':_post.locality,
            'area_1':_post.area_1,
            'sublocal_1': _post.sublocal_1,
            'sublocal_2': _post.sublocal_2,
            'sublocal_4': _post.sublocal_4,
            'addr':_post.addr,
            'addr_detail':_post.addr_detail,
            'empty_box': range(5-(_post.t2classpic_set.all().count())),
        }
        img_arr=[]
        for db_images in _post.t2classpic_set.all():
            img_info=[]
            contents = imgdb_to_uploadifle(LOCAL, db_images.image)
            img_info.append(db_images.id)
            img_info.append(db_images.image)
            img_info.append(contents)
            img_arr.append(img_info)
        teach_data['db_images']=img_arr

    elif request.method == "POST":
        locality=request.POST.get("locality", "").encode("utf-8")
        area_1=request.POST.get("area_1", "").encode("utf-8")
        sublocal_1=request.POST.get("sublocal_1", "").encode("utf-8")
        sublocal_2=request.POST.get("sublocal_2", "").encode("utf-8")
        sublocal_4=request.POST.get("sublocal_4", "").encode("utf-8")
        _state, create=check_state(request)
        addr=area_1+" "+locality+" "+sublocal_1+" "+sublocal_2+" "+sublocal_4
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
            'repeat': int(request.POST.get("repeat")),
            'perhour':int(request.POST.get("perhour")),
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
            'locality':locality,
            'area_1': area_1,
            'sublocal_1': sublocal_1,
            'sublocal_2': sublocal_2,
            'sublocal_4': sublocal_4,
            'addr':addr,
            'addr_detail':addr_detail,
        }
        img_arr=[]
        for db_images in _pre_fillpost.t2classpic_set.all():
            img_info=[]
            contents = imgdb_to_uploadifle(LOCAL, db_images.image)
            img_info.append(db_images.id)
            img_info.append(db_images.image)
            img_info.append(contents)
            img_arr.append(img_info)
        teach_data['db_images']=img_arr

        teachform=T2TeachClassForm(teach_data, instance=_pre_fillpost)
        prefill_intro=request.POST.get("intro_self").encode("utf-8")

        auth=False
        if _pre_fillpost.user == request.user or request.user.is_staff:
            auth = True
        img_valid=False
        imageform=T2ClassPicForm(teach_data, request.FILES)
        if imageform.is_valid() or len(request.POST.getlist("img_id")[0])>0:
            img_valid=True

        if teachform.is_valid() and auth:
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


            _old_class_img_set = T2ClassPic.objects.filter(teach_post=_teachpost)
            _old_card_img_set = T2CardPic.objects.filter(class_card=_classcard)
            if len(request.POST.getlist("img_id")[0])>0 :
                fst_img_id=request.POST.getlist("img_id")[0]
                _fst_img=T2ClassPic.objects.filter(id=fst_img_id)[0].image
                content=imgdb_to_uploadifle(LOCAL, _fst_img)
                request.FILES['card_img']=content
            elif request.FILES.getlist("image"):
                request.FILES['card_img']=request.FILES.getlist("image")[0]

            if _old_card_img_set.exists():
                _old_card_img_set.delete()
            i=0
            img_list=[]
            for old_class_img in _old_class_img_set:
                if unicode(old_class_img.id) not in request.POST.getlist("img_id"):
                    old_class_img.delete()

            imagelist=[]
            imageform=T2ClassPicForm(teach_data,  request.FILES)
            card_imageform=T2CardPicForm(teach_data, request.FILES)
            if imageform.is_valid():
                _imagelist=imageform.savefiles()
                _card_img=card_imageform.save_img()

            return render(request, TEMP.CLASS_MODIFY_FINISH_V2D1,{
                 "HTTP_HOST":HTTP_HOST,
                 "cl_card_id":_classcard.id,
            })

    return render(request, TEMP.CLASS_MODIFY_TEACH_V2D1, {
        "teachform":teachform,
        "imageform":imageform,
        "teach_data":teach_data,
        "class_num":class_num,
        "HTTP_HOST":HTTP_HOST,
        })

@login_required
@user_passes_test(host_check, login_url="/v2.1/user/host/apply/")
def modify_tut(request, class_num):
    HTTP_HOST=request.META["HTTP_HOST"]
    if request.method == "GET":
        tutform=T2TutClassForm()
        imageform=T2ClassPicForm()
        try :
            _post=T2TutClass.objects.get(pk=class_num)
            if _post.user != request.user and not request.user.is_staff:
                raise Http404("수정 가능한 사용자가 아닙니다.")
        except ObjectDoesNotExist:
            raise Http404("포스팅이 존재 하지 않습니다.")
        _user=User.objects.get(username=request.user)
        tut_data={
            "user":_user,
            "post":_post,
            "category":_post.category,
            "title":_post.title,
            "intro_line":_post.intro_line,
            "classtype":_post.classtype,
            'repeat':_post.repeat,
            'perhour':_post.perhour,
            'weekday':_post.weekday,
            'price':str(_post.price),
            'extra_price':str(_post.extra_price),
            'video':shard_url_picker(_post.video),
            'descript':_post.descript,
            'curri':_post.curri,
            'notic':_post.notic,
            'state':_post.state,
            'locality':_post.locality,
            'area_1':_post.area_1,
            'sublocal_1': _post.sublocal_1,
            'sublocal_2': _post.sublocal_2,
            'sublocal_4': _post.sublocal_4,
            'addr':_post.addr,
            'addr_detail':_post.addr_detail,
            'empty_box': range(5-(_post.t2classpic_set.all().count())),
        }
        img_arr=[]
        for db_images in _post.t2classpic_set.all():
            img_info=[]
            contents = imgdb_to_uploadifle(LOCAL, db_images.image)
            img_info.append(db_images.id)
            img_info.append(db_images.image)
            img_info.append(contents)
            img_arr.append(img_info)
        tut_data['db_images']=img_arr

    elif request.method == "POST":
        locality=request.POST.get("locality", "").encode("utf-8")
        area_1=request.POST.get("area_1", "").encode("utf-8")
        sublocal_1=request.POST.get("sublocal_1", "").encode("utf-8")
        sublocal_2=request.POST.get("sublocal_2", "").encode("utf-8")
        sublocal_4=request.POST.get("sublocal_4", "").encode("utf-8")
        _state, create=check_state(request)
        addr=area_1+" "+locality+" "+sublocal_1+" "+sublocal_2+" "+sublocal_4
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
            'repeat':int(request.POST.get("repeat")),
            'perhour':int(request.POST.get("perhour")),
            'weekday':request.POST.get("weekday"),
            'price':request.POST.get('price'),
            'extra_price':request.POST.get('extra_price'),
            'video':shard_url_picker(request.POST.get("video")),
            'descript':request.POST.get("descript"),
            'curri':request.POST.get("curri"),
            'notic':request.POST.get("notic"),
            'state':_state,
            'locality':locality,
            'area_1':area_1,
            'sublocal_1':sublocal_1,
            'sublocal_2':sublocal_2,
            'sublocal_4':sublocal_4,
            'addr':addr,
            'addr_detail':addr_detail,
        }
        img_arr=[]
        for db_images in _pre_fillpost.t2classpic_set.all():
            img_info=[]
            contents = imgdb_to_uploadifle(LOCAL, db_images.image)
            img_info.append(db_images.id)
            img_info.append(db_images.image)
            img_info.append(contents)
            img_arr.append(img_info)
        tut_data['db_images']=img_arr

        tutform=T2TutClassForm(tut_data, instance=_pre_fillpost)
        prefill_intro=request.POST.get("intro_self").encode("utf-8")

        auth=False
        if _pre_fillpost.user == request.user or request.user.is_staff:
            auth = True
        img_valid=False
        imageform=T2ClassPicForm(tut_data, request.FILES)

        if imageform.is_valid() or len(request.POST.getlist("img_id")[0])>0:
            img_valid=True
            imageform.errors['image']=imageform.error_class()


        if tutform.is_valid() and img_valid and auth:
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

            _old_class_img_set = T2ClassPic.objects.filter(tut_post=_tutpost)
            _old_card_img_set = T2CardPic.objects.filter(class_card=_classcard)
            if len(request.POST.getlist("img_id")[0])>0 :
                fst_img_id=request.POST.getlist("img_id")[0]
                _fst_img=T2ClassPic.objects.filter(id=fst_img_id)[0].image
                content=imgdb_to_uploadifle(LOCAL, _fst_img)
                request.FILES['card_img']=content
            elif request.FILES.getlist("image"):
                request.FILES['card_img']=request.FILES.getlist("image")[0]

            if _old_card_img_set.exists():
                _old_card_img_set.delete()
            i=0
            img_list=[]
            for old_class_img in _old_class_img_set:
                if unicode(old_class_img.id) not in request.POST.getlist("img_id"):
                    old_class_img.delete()

            imagelist=[]
            imageform=T2ClassPicForm(tut_data,  request.FILES)
            card_imageform=T2CardPicForm(tut_data, request.FILES)
            if imageform.is_valid():
                _imagelist=imageform.savefiles()
                _card_img=card_imageform.save_img()

            return render(request, TEMP.CLASS_MODIFY_FINISH_V2D1,{
                "HTTP_HOST":HTTP_HOST,
                "cl_card_id":_classcard.id,
                    })
    return render(request, TEMP.CLASS_MODIFY_TUT_V2D1, {
        "tutform":tutform,
        'imageform':imageform,
        "tut_data":tut_data,
        "class_num":class_num,
        "HTTP_HOST":HTTP_HOST,
    })

def create_review(request, class_num):

    HTTP_HOST=request.META["HTTP_HOST"]
    if request.method == "POST":
        if not request.user.is_authenticated():
            next=request.POST.get("next", "/")
            return HttpResponseRedirect("/v2.1/user/login?next="+next)
        _post=""
        _review=""
        review=request.POST.get("review", "")
        grade=request.POST.get("grade", "")
        _user=User.objects.get(username=request.user)
        classtype=request.POST.get("classtype", "")

        review_data={
            'classtype':classtype,
            "review":review,
            "grade":grade,
            "user":_user,
        }
        reviewform=T2ReviewForm(review_data)
        if classtype == "teach_class":
            _post=T2TeachClass.objects.get(pk=class_num)
            review_data["post"]=_post
            if reviewform.is_valid():
                _review=T2ClassReview(user=_user, host_user=_post.user,
                                  teach_post=_post, grade=grade,
                                  review=review)
                _review.save()
        elif classtype == "tut_class":
            _post=T2TutClass.objects.get(pk=class_num)
            review_data["post"]=_post
            if reviewform.is_valid():
                _review=T2ClassReview(user=_user, host_user=_post.user,
                        tut_post=_post, grade=grade,
                        review=review)
                _review.save()
        # return render(request, TEMP.TUT_POST_DETAIL_V2D1,{
        #     "post":_post,
        #     "review":reviewform,
        #     "HTTP_HOST":HTTP_HOST,
        # })
        return HttpResponseRedirect("/v2.1/class/"+str(_post.t2classcard_set.first().id))
    return Http404("잘못된 요청입니다.")

    # return HttpResponseRedirect("/")


@login_required
def modify_review(request, class_num):
    HTTP_HOST=request.META["HTTP_HOST"]
    if request.method == "POST":
        review_num=request.POST.get("review_num","")
        review=request.POST.get("review", "")
        grade=request.POST.get("grade", "")
        _user=User.objects.get(username=request.user)
        classtype=request.POST.get("classtype", "")
        review_data={
            'classtype':classtype,
            "review":review,
            "grade":grade,
            "user":_user,
        }
        reviewform=T2ReviewForm(review_data)

        if classtype == "teach_class":
            _review=T2ClassReview.objects.get(pk=review_num)
            _post=T2TeachClass.objects.get(pk=class_num)
            review_data["post"]=_post
            _review.review=review
            _review.grade=grade
            _review.save()
            return HttpResponseRedirect("/v2.1/class/"+str(_post.t2classcard_set.first().id))

        elif classtype == "tut_class":
            _review=T2ClassReview.objects.get(pk=review_num)
            _post=T2TutClass.objects.get(pk=class_num)
            review_data["post"]=_post
            _review.review=review
            _review.grade=grade
            _review.save()
            return HttpResponseRedirect("/v2.1/class/"+str(_post.t2classcard_set.first().id))

    return HttpResponseRedirect("/")

@login_required
def delete_review(request, review_num):
    HTTP_HOST=request.META["HTTP_HOST"]
    if request.method == "POST":
        _user=User.objects.get(username=request.user)
        classtype=request.POST.get("classtype", "")


        if classtype == "teach_class":
            _review=T2ClassReview.objects.get(pk=review_num)
            _post=_review.teach_post
            if _review.user == request.user:
                _review.is_active=False
                _review.save()
            return HttpResponseRedirect("/v2.1/class/"+str(_post.t2classcard_set.first().id))
            # return render(request, TEMP.TEACH_POST_DETAIL_V2D1,{
            #     "post":_post,
            #     "HTTP_HOST":HTTP_HOST,
            #
            # })

        elif classtype == "tut_class":
            _review=T2ClassReview.objects.get(pk=review_num)
            _post=_review.tut_post
            if _review.user == request.user:
                _review.is_active=False
                _review.save()
            return HttpResponseRedirect("/v2.1/class/"+str(_post.t2classcard_set.first().id))
            # return render(request, TEMP.TUT_POST_DETAIL_V2D1,{
            #     "post":_post,
            #     "HTTP_HOST":HTTP_HOST,
            # })

    return HttpResponseRedirect("/")


def class_post_detail(request, class_num):
    HTTP_HOST=request.META["HTTP_HOST"]
    if request.method == "GET":
        _postcard=T2ClassCard.objects.filter(pk=class_num)[0]
        _post=""
        if _postcard.classtype == "tutclass":
            _post=_postcard.tut_post
            _reviews=_post.t2classreview_set.filter(is_active=True)
            return render(request, TEMP.TUT_POST_DETAIL_V2D1,{
                "post":_post,
                "reviews":_reviews,
                "HTTP_HOST":HTTP_HOST,
                "next":"/v2.1/class/"+str(class_num)
            })

        else:
            _post=_postcard.teach_post
            _reviews=_post.t2classreview_set.filter(is_active=True)
            return render(request, TEMP.TEACH_POST_DETAIL_V2D1,{
                "post":_post,
                "reviews":_reviews,
                "HTTP_HOST": HTTP_HOST,
                "next":"/v2.1/class/"+str(class_num)
            })
    else :
        raise Http404("잘못된 요청 입니다.")


@login_required
@user_passes_test(host_check, login_url="/v2.1/user/host/apply/")
def class_onoff(request ,class_type, card_num, pro_user_num):

    _classcard=get_object_or_404(T2ClassCard, pk=card_num)
    if _classcard.user != request.user and not request.user.is_staff:
        return Http404("잘못된 요청입니다.")

    if class_type == "tutclass":
        _post=_classcard.tut_post
    else:
        _post=_classcard.teach_post

    if _classcard.is_open == False\
            and _classcard.deadline_over == False \
            and _classcard.wr_done == True:
        _classcard.is_open=True
        _post.is_open=True
        _classcard.save()
        _post.save()
    elif _classcard.is_open == True or _classcard.deadline_over == True:
        _classcard.is_open=False
        _classcard.save()
        _post.is_open=False
        _post.save()


    return HttpResponseRedirect("/v2.1/user/profile/%s/class_check" %(pro_user_num))





def check_state(request):

    if request:
        state=""
        locality=request.POST.get("locality", "").encode("utf-8")
        area_1=request.POST.get("area_1", "").encode("utf-8")
        sublocal_1=request.POST.get("sublocal_1", "").encode("utf-8")
        local_list=[]
        local_list.append(area_1)
        local_list.append(locality)

        #서울 동북
        zone_1 = ['도봉구','노원구','강북구','중랑구','광진구','동대문구', '성북구','성동구']
        #서울 서북
        zone_2 = ['은평구','마포구', '서대문']
        #서울 도심
        zone_3 = ['종로구','중구','용산구']
        #서울 남서
        zone_4 = ['강서구','양천구','구로구','영등포구','동작구','관악구']
        #서울 강남
        zone_5 = ['송파구','강남구','서초구']

        #경기 남부-수원,안산,안양
        zone_6 = ['수원시', '화성시', '오산시', '평택시', '안양시', '군포시', '의왕시',
                  '과천시', '안산시', '시흥시']
        #경기 동부-성남/남양주/용인
        zone_7 = ['성남시', '광주시', '용인시', '구리시', '하남시','남양주시',
                  '양평군', '강평군']
        #경기 북부-파주/의정부/고양(일산)
        zone_8 = ['고양시', '김포시','파주시', '양주시', '포천시', '의정부시']
        #인천/부천
        zone_9 = ["인천광역시", '부천시']


        for local in local_list:
            if local in ["서울특별시"]:
                state="zone_1"
                break
                # if sublocal_1 in zone_1:
                #     state="zone_1"
                #     break
                # elif sublocal_1 in zone_2:
                #     state="zone_2"
                #     break
                # elif sublocal_1 in zone_3:
                #     state="zone_3"
                #     break
                # elif sublocal_1 in zone_4:
                #     state="zone_4"
                #     break
                # elif sublocal_1 in zone_5:
                #     state="zone_5"
                #     break
            elif local in ["경기도", "인천광역시"]:
                state="zone_2"
                # if locality in zone_5:
                #     state="zone_6"
                #     break
                # elif locality in zone_6:
                #     state="zone_7"
                #     break
                # elif locality in zone_7:
                #     state="zone_8"
                #     break
                # elif locality in zone_8:
                #     state="zone_9"
                #     break
            elif local in ["부산광역시"]:
                state="zone_3"
                break
            elif local in ['울산광역시','경상남도',
                           '대구광역시', '경상북도',
                           '대전광역시','세종특별자치시', '충청북도', '충청남도',
                           '광주광역시', '전라북도', '전라남도',
                           '강원도', '제주특별자치도']:
                state="etc"
                break

        _state=State.objects.get_or_create(state=state)
        return _state
    else :
        return False

def imgdb_to_uploadifle(local, dburl):

    if local:
        url_set = "http://localhost:8000/userphoto/media/"
    else:
        url_set= "http://diytec.beta.s3.amazonaws.com/uploads/"

    img_info=[]
    url =url_set+str(dburl)
    img_res = requests.get(url)
    img = Image.open(StringIO(img_res.content))
    imgstring = StringIO()
    img.save(imgstring, "PNG")
    newfile=InMemoryUploadedFile(imgstring, None, 'temp.png', 'image/png', imgstring.len, None)

    return newfile
