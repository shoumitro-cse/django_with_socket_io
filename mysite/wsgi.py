"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import socketio
from mysite.server import sio

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

static_files = {
   '/static/': 'static/',
}

#application = get_wsgi_application()
django_app = get_wsgi_application()
application = socketio.WSGIApp(socketio_app=sio, wsgi_app=django_app, static_files=static_files)
