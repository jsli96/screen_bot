import time
import socketio
# import cv2 as cv
import base64
from gpiozero import *
# from picamera import Picamera
MOTOR_A_PWM = 'GPIO12'     # PWM input for extension motor
MOTOR_A_PHASE = 'GPIO5'    # Phase input for extension motor
MOTOR_B_PWM = 'GPIO13'     # PWM input for rotation motor
MOTOR_B_PHASE = 'GPIO6'    # Phase input for rotation motor
ROTATION_C1 = 'GPIO21'     # Motor encoder C1
ROTATION_C2 = 'GPIO20'     # Motor encoder C2
ROTATION_VCC = 'GPIO16'    # Encoder power line
# camera = Picamera()
URL_LOCAL = 'http://127.0.0.1:5000/'
URL_CLOUD = 'https://screen-bot-proj.herokuapp.com/'
E_MOTOR = PhaseEnableMotor(MOTOR_A_PHASE, MOTOR_A_PWM, pwm=True)    # Set up extension motor
R_MOTOR = PhaseEnableMotor(MOTOR_B_PHASE, MOTOR_B_PWM, pwm=True)    # Set up rotation motor
VCC = DigitalOutputDevice(ROTATION_VCC, initial_value=True)
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


# sio.connect('http://127.0.0.1:5000/')
# sio.emit('This is test in main function', "It\'s me")
# sio.wait()
R_MOTOR.backward(speed=0)
E_MOTOR.forward(speed=1)
time.sleep(3)
R_MOTOR.forward(speed=1)
E_MOTOR.backward(speed=0)
time.sleep(3)
