#It just needs to install more packages here.
# pip install gevent-websocket
# pip install eventlet

# pip install "python-socketio[client]"
# pip install "python-socketio[asyncio_client]" # for asyncio

import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')
    sio.emit('begin_chat', 1234567)

@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})

@sio.event
def connect_error(data):
    print("The connection failed!")
    
@sio.event
def disconnect():
    print('disconnected from server')

@sio.event
def my_response(data):
    print("\n\nmy_response data : ", data)
    
    
sio.connect('http://localhost:8000')
sio.wait
#sio.emit('my_response', {'foo': 'bar'})
#sio.emit('begin_chat', 1234567)
#sio.emit('exit_chat', 1234567)
# sio.send("response")


