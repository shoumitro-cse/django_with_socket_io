import os
import socketio

# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed

async_mode = 'eventlet'
basedir = os.path.dirname(os.path.realpath(__file__))
mgr = socketio.RedisManager('redis://')
sio = socketio.Server(logger=True, async_mode=async_mode, client_manager=mgr)