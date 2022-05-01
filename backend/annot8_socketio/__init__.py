"""
example code from
https://github.com/miguelgrinberg/python-socketio/tree/main/examples/server/wsgi
"""

import socketio
import logging

from django.conf import settings

async_mode = 'eventlet'
cors_allowed_origins = settings.CORS_ORIGIN_WHITELIST or ["*"]

sio = socketio.Server(
    async_mode=async_mode,
    cors_allowed_origins=cors_allowed_origins
)

logging.info(f"{cors_allowed_origins=}")
