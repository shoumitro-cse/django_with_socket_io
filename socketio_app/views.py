# https://python-socketio.readthedocs.io/en/latest/client.html
# https://socket.io/docs/v4/client-api/


# pip install --upgrade pip setuptools
# gunicorn -k eventlet -w 1 mysite.wsgi

"""
/home/shoumitro/.pyenv/versions/3.8.12/bin/python -m venv env
source ./env/bin/activate
python -V

pip install "python-socketio[client]"
pip install gunicorn gevent-websocket eventlet
pip install https://github.com/eventlet/eventlet/archive/master.zip

gunicorn --log-level INFO --thread 50 mysite.wsgi
gunicorn -w 1 --worker-class eventlet  mysite.wsgi
gunicorn --worker-class eventlet -w 1 mysite.wsgi --reload

# works fine
gunicorn --worker-class eventlet -w 1 mysite.wsgi
pip uninstall gunicorn
pip uninstall eventlet
pip install gunicorn==20.1.0
pip install eventlet==0.30.2
pip install https://github.com/eventlet/eventlet/archive/master.zip
"""

# for threading
# gunicorn --log-level INFO --thread 50 mysite.wsgi

# It just needs to install more packages here.
# pip install gevent-websocket
# pip install eventlet

# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed
async_mode = 'eventlet'

import os

from django.http import HttpResponse
import socketio
from django.shortcuts import get_object_or_404, render, redirect

basedir = os.path.dirname(os.path.realpath(__file__))
sio = socketio.Server(logger=True, async_mode=async_mode)
thread = None


def index(request):
    # global thread
    # if thread is None:
    #    thread = sio.start_background_task(background_thread)
    return render(request, 'index.html')


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        sio.sleep(10)
        count += 1
        sio.emit('my_response', {'data': 'Server generated event'},
                 namespace='/test')


@sio.event
def my_event(sid, event_data):
    sio.emit('my_response', {'data': event_data['data']}, room=event_data['room_id'])


@sio.event
def my_broadcast_event(sid, message):
    sio.emit('my_response', {'data': message['data']})


@sio.event
def join(sid, message):
    sio.enter_room(sid, message['room'])
    sio.emit('my_response', {'data': 'Entered room: ' + message['room']},
             room=sid)


@sio.event
def leave(sid, message):
    sio.leave_room(sid, message['room'])
    sio.emit('my_response', {'data': 'Left room: ' + message['room']},
             room=sid)


@sio.event
def close_room(sid, message):
    sio.emit('my_response',
             {'data': 'Room ' + message['room'] + ' is closing.'},
             room=message['room'])
    sio.close_room(message['room'])


@sio.event
def my_room_event(sid, message):
    sio.emit('my_response', {'data': message['data']}, room=message['room'])


@sio.event
def disconnect_request(sid):
    sio.disconnect(sid)
    print("\n\ndisconnect sid: ", sid)
    print()


@sio.event
def connect(sid, environ):
    # sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)
    print("\nconnect sid: ", sid)
    print()


@sio.event
def disconnect(sid):
    print('Client disconnected')
    print("\ndisconnect sid: ", sid)
    print()


@sio.event
def begin_chat(sid, room_id):
    sio.enter_room(sid, room_id)
    print()
    sio.emit('my_response', {'data': 'begin_chat', 'room_id': room_id}, room=room_id)
    print("\nbegin_chat sid, room_id: ", sid, room_id)
    print()


@sio.event
def exit_chat(sid, room_id):
    sio.leave_room(sid, room_id)
    print("\nexit_chat sid, room_id: ", sid, room_id)
    print()


# @sio.event
# def my_response(sid, data):
#    print("\nmy_response sid, data : ", sid, data)
#    print()


class MyCustomNamespace(socketio.Namespace):
    def on_connect(self, sid, environ):
        print("\n on_connect sid: ", sid)

    def on_disconnect(self, sid):
        print("\n on_disconnect sid: ", sid)

    def on_my_event(self, sid, event_data):
        self.emit('my_response', {'data': event_data['data']}, room=event_data['room_id'])


sio.register_namespace(MyCustomNamespace('/test'))
