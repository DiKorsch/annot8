import logging

from django.conf import settings
from django.core.management.commands.runserver import Command as RunCommand
from annot8_socketio import sio

class Command(RunCommand):
    help = 'Run the Socket.IO server'

    def handle(self, *args, **options):
        if sio.async_mode == 'threading':
            super(Command, self).handle(*args, **options)

        elif sio.async_mode == 'eventlet':
            run_eventlet()

        elif sio.async_mode == 'gevent':
            run_gevent()

        elif sio.async_mode == 'gevent_uwsgi':
            logging.warning('Start the application through the uwsgi server. Example:')
            logging.warning('uwsgi --http :5000 --gevent 1000 --http-websockets '
                  '--master --wsgi-file annot8/wsgi.py --callable '
                  'application')
        else:
            logging.error(f'Unknown async_mode: {sio.async_mode}')

def run_eventlet():

    import eventlet
    import eventlet.wsgi
    from annot8.wsgi import application
    listener = eventlet.listen(('', settings.SOCKETIO_PORT))
    eventlet.wsgi.server(listener, application)

def run_gevent():

    # deploy with gevent
    from gevent import pywsgi
    from annot8.wsgi import application

    try:
        from geventwebsocket.handler import WebSocketHandler

        pywsgi.WSGIServer(
            ('', settings.SOCKETIO_PORT), application,
            handler_class=WebSocketHandler).serve_forever()
    except ImportError:
        pywsgi.WSGIServer(('', settings.SOCKETIO_PORT), application).serve_forever()

