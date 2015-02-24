"""
WSGI config for DIY_tool project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
local = True

if local:
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DIY_tool.settings")

    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
else :
    import os
    import sys

    ##setting uer virtualenv##
    activate_this = '/home/ubuntu/.virtualenv/diy_tec/bin/activate_this.py'
    execfile(activate_this, dict(__file__=activate_this))
    ##--##
    sys.path.append("/opt/diyroot")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DIY_tool.settings")
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
