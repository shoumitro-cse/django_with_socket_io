import os
import socketio

"""
set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
force a mode else, the best mode is selected automatically from what's
installed.
"""

""""
The logger argument controls logging related to the Socket.IO protocol, while engineio_logger 
controls logs that originate in the low-level Engine.IO transport. These arguments can be set 
to True to output logs to stderr, or to an object compatible with Python’s logging package 
where the logs should be emitted to. A value of False disables logging.
"""

async_mode = 'eventlet'
basedir = os.path.dirname(os.path.realpath(__file__))
mgr = socketio.RedisManager('redis://')
sio = socketio.Server(
    logger=True,
    async_mode=async_mode,
    client_manager=mgr,
    # engineio_logger=True
)
