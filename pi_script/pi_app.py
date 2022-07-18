import time
import socketio
# import cv2 as cv
import base64
from gpiozero import *
from time import sleep
# from picamera import Picamera
MOTOR_A_IN_1 = 26
MOTOR_A_IN_2 = 21
MOTOR_B_IN_1 = 23
MOTOR_B_IN_2 = 22
# camera = Picamera()
URL_LOCAL = 'http://127.0.0.1:5000/'
URL_CLOUD = 'https://screen-bot-proj.herokuapp.com/'
sio = socketio.Client()


def send_img():
    img = cv.imread("photo/test.png", cv.IMREAD_GRAYSCALE)  # Read first image
    img = cv.resize(img, (0, 0), fx=0.5, fy=0.5)
    size, data = cv.imencode('.png', img)
    data = base64.b64encode(data)
    sio.emit('img_data', data)


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


@sio.on('receive finished')
def disconnect():
    sio.disconnect()


@sio.on('request img')
def start_send_img(data):
    print(data)
    send_img()
    return 'OK'


def main():
    # sio.connect('http://127.0.0.1:5000/')
    # sio.emit('This is test in main function', "It\'s me")
    # sio.wait()
    motor_1 = PhaseEnableMotor(MOTOR_A_IN_1, MOTOR_A_IN_2)



motor_1 = PhaseEnableMotor(26, 21)
motor_1.backward()
