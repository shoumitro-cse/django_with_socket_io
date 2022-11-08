"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
import socketio
from mysite.server import asio

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

static_files = {
   '/static/': 'static/',
}

# application = get_asgi_application()
asgi_django_app = get_asgi_application()
application = socketio.ASGIApp(socketio_server=asio, other_asgi_app=asgi_django_app, static_files=static_files)

