"""
WSGI config for AIRPACT_Fire project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AIRPACT_Fire.settings")

# application = get_wsgi_application()
