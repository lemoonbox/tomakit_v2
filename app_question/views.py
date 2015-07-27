from django.shortcuts import render

from django.shortcuts import \
    loader,\
    render
from django.contrib.auth.decorators import \
    login_required
from django.contrib.auth.models import \
    User
from django.http import \
    HttpResponseRedirect,\
    HttpResponse, \
    Http404

from app_question.form import CreateQItem
from app_comminfo.models import Category, State
from app_question.models import QItem, QPic


from DIY_tool import template_match as TEMP

# Create your views here.

@login_required
def create_q_item(request):

    if request.method == "GET":
        create_qform = CreateQItem()

    elif request.method == "POST":
        user = User.objects.get(username=request.user)
        create_qform = CreateQItem(request.POST)
        category= request.POST['category']
        state = request.POST['state']
        photos = request.FILES.getlist("Qphoto", "")

        if create_qform.is_valid():
            _qitempost = create_qform.save(commit=False)
            _qitempost.djgouser=request.user
            _qitempost.save()
            _category=Category.objects.get_or_create(category=category)
            _state = State.objects.get_or_create(state=state)
            _qitempost.category =_category
            _qitempost.state = _state
            _qitempost.save()

            for photo in photos:
                _qpic = QPic(user=user,qitem=_qitempost,pic=photo)
                _qpic.save()
                _qpic.category.add(_category[0])
                _qpic.save()

            return HttpResponseRedirect("/v2/question/item/{0}".format(_qitempost.id))


    return render(request, TEMP.V2_CREATE_QITEM,{
        'create_qform':create_qform,
    })


def qitem_detail(request, qitem_num):

    if request.method == "GET":
        try:
            _qitempost = QItem.objects.get(pk=qitem_num)
        except _qitempost.DoesNotExist:
            raise Http404("post does not exist")
    return render(request, TEMP.V2_DETAIL_QITEM,
        {
            'qitem_post':_qitempost
        })
