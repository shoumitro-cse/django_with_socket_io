from django.shortcuts import render
from mysite.server import sio
import socketio


def index(request):
    # thread = None
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
    print("\nconnect sid: ", sid)
    # print(environ)
    # username = authenticate_user(environ)
    username = "shoumitro26"
    sio.save_session(sid, {'username': username})


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


@sio.event
def message(sid, data):
    session = sio.get_session(sid)
    print('message from ', session['username'])


@sio.event(namespace='/chat')
def sms_event(sid, data):
    pass


@sio.on('my custom event', namespace='/chat')
def my_custom_event(sid, event_data):
    print("\n my_custom_event sid: ", sid)
    sio.emit('my_response', {'data': event_data['data']}, room=event_data['room_id'])


class MyCustomNamespace(socketio.Namespace):
    def on_connect(self, sid, environ):
        print("\n on_connect sid: ", sid)
        # username = authenticate_user(environ)
        self.save_session(sid, {'username': "shoumitro26"})

    def on_disconnect(self, sid):
        print("\n on_disconnect sid: ", sid)

    def on_begin_chat(self, sid, room_id):
        self.enter_room(sid, room_id)

    def on_exit_chat(self, sid, room_id):
        self.leave_room(sid, room_id)

    def on_message(self, sid, event_data):
        session = self.get_session(sid)
        # print('message from ', session['username'])
        self.emit('my_response', {'data': event_data, 'username': session['username']},
                  room=event_data['room_id'])

    def on_my_event(self, sid, event_data):
        print("\n on_my_event data: ", event_data)
        self.emit('my_response', {'data': event_data}, room=event_data['room_id'])


# register namespace class
sio.register_namespace(MyCustomNamespace('/test'))