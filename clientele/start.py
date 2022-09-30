import time

from clientele import sio, utils, create_app


def call_back():
    print('回复了')


@sio.on('returnSystem')
def my_system_info(data):
    print(data)


@sio.on('test')
def test(data):
    print(data)


class ReGetSystemUtilities(utils.GetSystemUtilities):

    def reported(self):
        sio.emit('system', self.get)
        # sio.send(self.get, callback=call_back)


token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJDb2tlIiwidXNlcl9pZCI6MSwiZGV2aWNlIjoid2luZG93czEw' \
        'IiwiZXhwIjpudWxsfQ.BH_r1vpAN7_gnz0cSHsKxPlrbpKz2NjihI7KeBUASpw'


create_app(token)
sio.emit('joinRoom', {'roomId': 'Windows'}, callback=call_back)
ReGetSystemUtilities(daemon=True).start()
sio.emit('test')
