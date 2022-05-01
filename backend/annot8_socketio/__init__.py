"""
example code from
https://github.com/miguelgrinberg/python-socketio/tree/main/examples/server/wsgi
"""

import socketio

from django.conf import settings

async_mode = 'eventlet'

sio = socketio.Server(
    async_mode=async_mode,
    cors_allowed_origins=settings.ALLOWED_HOSTS or ["*"]
)
