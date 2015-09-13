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
    T2TutClassForm

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

    if request.method == "GET":
        pass

    elif request.method == "POST":
        pass

    return render(request, TEMP.CLASS_CREATE_TUT_V2D1,{

    })


def create_teach(request, class_num):
    title=""
    if request.method == "GET":
        teachform=T2TeachClassForm()
        title=request.GET.get("title")
    elif request.method == "POST":
        pass
    return render(request, TEMP.CLASS_CREATE_TEACH_V2D1,{
        "teachform":teachform,
        "title":title,
        "class_num":class_num,
    })