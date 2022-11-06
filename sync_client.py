import socketio

sio = socketio.Client()
room_id = 1234567


class MyCustomNamespace(socketio.ClientNamespace):
    def on_connect(self):
        self.emit('begin_chat', room_id)
        print('connection established')

    def on_disconnect(self):
        print('disconnected')

    def on_my_response(self, data):
        print("\nmy_response data : ", data)


sio.register_namespace(MyCustomNamespace('/test'))

sio.connect('http://localhost:8000', namespaces=['/test'])
sio.wait









# @sio.event
# def connect():
#     print('connection established')
#     sio.emit('begin_chat', room_id)
#
#
# @sio.event
# def my_message(data):
#     print('message received with ', data)
#     sio.emit('my response', {'response': 'my response'})
#
#
# @sio.event
# def connect_error(data):
#     print("The connection failed!")
#
#
# @sio.event
# def disconnect():
#     print('disconnected from server')
#
#
# @sio.event
# def my_response(data):
#     print("\n\nmy_response data : ", data)


# sio.connect('http://localhost:8000')
# sio.connect('http://localhost:8000', namespaces=['/test'])
# sio.wait


# sio.emit('my_response', {'foo': 'bar'})
# sio.emit('begin_chat', 1234567)
# sio.emit('exit_chat', 1234567)
# sio.send("response")


