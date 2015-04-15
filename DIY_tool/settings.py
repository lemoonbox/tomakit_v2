"""
Django settings for DIY_tool project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS ={
    os.path.join(BASE_DIR, 'templates'),
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sj)7m^^1u$9=s40&8de&z#$alfgx(k6fztu3gj(w2^pdsnne6n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
LOCAL = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

###setting for celery####close/not user redis anymore
# import djcelery
# djcelery.setup_loader()
# BROKER_URL = 'redis://localhost:6379/0'
# CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
#####setting for celery end###

###setting for celery &rabbitmq
if LOCAL:
    import djcelery
    djcelery.setup_loader()
    BROKER_URL='amqp://guest:guest@localhost:5672//'
else:
    import djcelery
    djcelery.setup_loader()
    BROKER_URL='amqp://moon:1234@localhost:5672//'
    CELERY_IMPORTS =('userapp.tasks')


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'userapp',
    'app_idealine',
    #'social.apps.django_app.default',
    'djcelery',
    'storages',
    'django_summernote',
    'app_post'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    #'social.apps.django_app.context_processors.backends',
    #'social.apps.django_app.context_processors.login_redirect',
)

####facebook auth####
"""
AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)


SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/user/profile'
SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_FACEBOOK_KEY = '1035953116420715'
SOCIAL_AUTH_FACEBOOK_SECRET = '84ef6ed0e0815ffea885ea022cdc6768'
SESSION_SERIALIZER='django.contrib.sessions.serializers.PickleSerializer'
###facebook auth end ###
"""
ROOT_URLCONF = 'DIY_tool.urls'

WSGI_APPLICATION = 'DIY_tool.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

if LOCAL :
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else :
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'testdb',
            'USER': 'root',
            'PASSWORD':'ok123456',
            'HOST':'dic-tec3.cfxqbzsbzi3i.ap-northeast-1.rds.amazonaws.com',
            'PORT':'3306',
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# email with TLS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_POST = 587
EMAIL_HOST_USER = 'makerecipe@gmail.com' # gmail login account.. user@example.com
EMAIL_HOST_PASSWORD = 'maketeee15'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/


####------------------default login path----------------------####
LOGIN_REDIRECT_URL = '/user/profile'
LOGIN_URL = '/user/login/'
LOGOUT_URL = '/user/logout/'

####------------------serve static/media file----------------------####
#S3serve settings
AWS_HEADERS = {
    'Expires' : 'Thu, 31 Dec 2099 20:00:00 GMT',
    'Cashe-Control' : 'max-age=94608000',
}
#S3 acess_key
AWS_STORAGE_BUCKET_NAME = 'diytec.beta'
AWS_ACCESS_KEY_ID = 'AKIAJG4KYTAON2HRQB7Q'
AWS_SECRET_ACCESS_KEY = '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'
AWS_S3_SECURE_URLS = False
AWS_QUERYSTRING_AUTH = False


if LOCAL :
    #local_static
    STATIC_URL = '/static/'
    STATICFILES_DIRS=(os.path.join(BASE_DIR, 'static_local'),)
    #local_media
    MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
    MEDIA_URL = '/userphoto/media/'

    SUMMERNOTE_CONFIG = {
    'lang': 'ko-KR',}

else :
    STATIC_URL = '/static/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')


    STATICFILES_DIRS=(os.path.join(BASE_DIR, 'static_local'),)
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    STATICFILES_LOCATION = 'static'
    STATICFILES_STORAGE = 'DIY_tool.custom_storages.StaticStorage'
    #It's for summernote
    STATIC_URL = "http://%s/" % AWS_S3_CUSTOM_DOMAIN

    MEDIAFILES_LOCATION = 'uploads'
    DEFAULT_FILE_STORAGE = 'DIY_tool.custom_storages.MediaStorage'
    MEDIA_URL = "http://%s/uploads/" % AWS_S3_CUSTOM_DOMAIN

    SUMMERNOTE_CONFIG = {
        'lang': 'ko-KR',
        #'attachment_storage_class': S3BotoStorage,
         }
