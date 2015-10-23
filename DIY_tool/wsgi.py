"""
WSGI config for DIY_tool project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
LOCAL = True

if LOCAL:
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DIY_tool.settings")

    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
else :
    import os
    import sys

    ##setting uer virtualenv##
    #amazon
    #activate_this = '/home/ubuntu/.virtualenvs/diy_tec/bin/activate_this.py'
    #conoha
    activate_this = '/opt/webroot/.virtualenvs/diy_tec/bin/activate_this.py'
    execfile(activate_this, dict(__file__=activate_this))
    #amazon
    #sys.path.append("/opt/diyroot")

    #conoha
    sys.path.append("/opt/webroot")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DIY_tool.settings")
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
