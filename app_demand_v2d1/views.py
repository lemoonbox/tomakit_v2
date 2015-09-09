from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from DIY_tool import template_match as TEMP
from app_demand_v2d1.forms import DemandForm
# Create your views here.
@login_required
def demand_create(request, demand_num=0):

    HTTP_HOST=request.META["HTTP_HOST"]
    if request.method == "GET":
        demandform=DemandForm()

        return render(request, TEMP.DEMAND_CREATE_V2D1,{
            'demandform':demandform,
            'HTTP_HOST':HTTP_HOST,
        })

    elif request.method == "POST":
        data={
            'category':request.POST.get('category', 'nodata'),
            'title':request.POST.get('title', 'nodata'),
            'descript':request.POST.get('descript', 'nodata'),
            'goal':request.POST.get('goal','nodata'),
            'weekday':request.POST.get('weekday', 'nodata'),
            'state':request.POST.get('state', 'nodata'),
            'local':request.POST.get('local', 'nodata'),
            'min_price':request.POST.get('min_price', 'nodata'),
            'max_price':request.POST.get('max_price', 'nodata')
        }
        demandform=DemandForm(data)

        if demandform.is_valid():
            print "is_OK"

        else:
            print "is_nok"




        return render(request, TEMP.DEMAND_CREATE_V2D1,{
        'HTTP_HOST':HTTP_HOST,
        })

