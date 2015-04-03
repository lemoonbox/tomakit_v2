from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import \
    login_required
from django.template import\
    Context


@login_required
def classcreate(request):

    ctx = Context({
        'error':None
    })
    error = False

    if request.method == "GET":
        class_form =ClassCreateForm()
        classpic_form = ClassPicCreateForm()
        class_detail_form = ClassdetailForm()


    elif request.method =="POST":
        pass


    return render(request, 'app_class/create_class_post.html',
        {
            'class_createform':class_form,
            'classpic_createform':classpic_form,
            'class_detailform': class_detail_form,
        })