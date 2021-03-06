from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from social.apps.django_app import urls


from userapp import urls as user_urls
from app_post import urls as post_urls
from app_idealine import urls as idealine_urls
from app_class import urls as class_urls


from app_user import urls as v2_user_urls
from app_question import urls as v2_question_urls
from app_board import urls as v2_board_urls

#v2.1
from app_board_v2d1 import urls as index_urls_v2d1
from app_user_v2d1 import urls as user_urls_v2d1
from app_demand_v2d1 import urls as demand_urls_v2d1
from app_class_v2d1 import urls as class_urls_v2d1
from app_payment_v2d1 import urls as payment_urls_v2d1
handler404='app_post.views.handler404'
handler500='app_post.views.handler500'

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include(user_urls)),
    url(r'^class/', include(class_urls)),
    url(r'^post/', include(post_urls)),
    url(r'^idealine/', include(idealine_urls)),

    url(r'^v2/user/', include(v2_user_urls)),
    url(r'^v2/question/', include(v2_question_urls)),
    url(r'^v2/board/', include(v2_board_urls)),

    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #v2.1
    url(r"^$", 'app_board_v2d1.views.mainpage', name='index'),
    url(r"^v2.1/$", 'app_board_v2d1.views.mainpage', name='main'),
    url(r'^v2.1/board/', include(index_urls_v2d1)),
    url(r'^v2.1/user/', include(user_urls_v2d1)),
    url(r'^v2.1/demand/', include(demand_urls_v2d1)),
    url(r'^v2.1/class/', include(class_urls_v2d1)),
    url(r'^v2.1/payment/', include(payment_urls_v2d1)),
)

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

