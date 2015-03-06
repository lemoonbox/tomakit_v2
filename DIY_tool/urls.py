from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
import settings as appset

import django_summernote.urls



from userapp import urls as user_urls
from app_class import urls as class_urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DIY_tool.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include(user_urls)),
    url(r'^class/', include(class_urls)),
    #url(r'', include('social.apps.django_app.urls', namespace='social')),

    url(r'^summernote/', include('django_summernote.urls')),



)

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)