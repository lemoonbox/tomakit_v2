from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from DIY_tool import \
    template_match as TEMP
from app_comminfo.models import \
    State, \
    Category
from app_demand_v2d1.forms import\
    DemandForm
from app_demand_v2d1.models import T2ClassDemand
# Create your views here.

@login_required
def demand_create(request, demand_num=0):
    demand_data={}
    HTTP_HOST=request.META["HTTP_HOST"]
    if request.method == "GET":
        demandform=DemandForm()

    elif request.method == "POST":
        demand_data={
            'user':request.user,
            'category':request.POST.get('category', ''),
            'title':request.POST.get('title', ''),
            'descript':request.POST.get('descript', ''),
            'goal':request.POST.getlist('goal',''),
            'weekday':request.POST.get('weekday', ''),
            'state':request.POST.get('state', ''),
            'local':request.POST.get('local', ''),
            'mobile1':request.POST.get('mobile1',''),
            'mobile2':request.POST.get('mobile2',''),
            'mobile':request.POST.get('mobile1','')+
                    request.POST.get('mobile2',''),
            'min_price':request.POST.get('min_price', ''),
            'max_price':request.POST.get('max_price', '')
        }
        demandform=DemandForm(demand_data)

        if demandform.is_valid():
            _demandpost=demandform.save(commit=True)


    return render(request, TEMP.DEMAND_CREATE_V2D1,{
        'demandform':demandform,
        'HTTP_HOST':HTTP_HOST,
        'demand_data':demand_data
    })

