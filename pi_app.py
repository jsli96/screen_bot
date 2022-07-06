import requests
import sys
import socketio
URL_LOCAL = 'http://127.0.0.1:5000/'
URL_CLOUD = 'https://screen-bot-proj.herokuapp.com/'
sio = socketio.Client()


@sio.event
def connect():
    print('my sid is: ' + sio.sid)
    print('connection established')


@sio.event
def connect_error(error):
    print(error)


@sio.event
def disconnect():
    print("disconnected")


@sio.on('request img')
def send_img(data):
    print(data)
    initial_connect = requests.get('http://127.0.0.1:5000/pi_send_img/')
    return 'OK'


def main():
    sio.connect('http://127.0.0.1:5000/')
    sio.emit('This is test in main function', "It\'s me")
    sio.wait()


if __name__ == '__main__':
    main()


