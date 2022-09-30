import socketio
import socket
import time

sio = socketio.Client()


# @sio.on('message', namespace='/test')
# def my_event_handler(data):
#     print(data)

@sio.on('returnSystem')
def my_system_info(data):
    print(data)


token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJNYWMiLCJ1c2VyX2lkIjoyLCJkZXZpY2' \
        'UiOiJNYWMxNCIsImV4cCI6bnVsbH0.fSiTCXvhYS8C338YMvva2feXW24qNnGBK8slD1iEnsQ'

sio.connect('http://127.0.0.1:5000', {'token': token})
time.sleep(10)
print('加入房间后展示性能消息')
sio.emit('joinRoom', {'roomId': 'Windows'})
