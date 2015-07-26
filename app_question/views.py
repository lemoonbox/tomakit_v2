from django.shortcuts import render

from django.shortcuts import \
    loader,\
    render
from django.contrib.auth.decorators import \
    login_required


from app_question.form import CreateQItem



from DIY_tool import template_match as TEMP

# Create your views here.

@login_required
def create_q_item(request):

    if request.method == "GET":
        create_qform = CreateQItem()

    elif request.method == "POST":
        create_qform = CreateQItem(request.POST)

        if create_qform.is_valid():
            _qitempost = create_qform.save(commit=False)
            _qitempost.djgouser=request.user
            _qitempost.save()

    return render(request, TEMP.V2_CREATE_QITEM,{
        'create_qform':create_qform,
    })
