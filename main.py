from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import logging
from imageMatch import *
import base64

app = Flask(__name__)
socketio = SocketIO(app)
PI_STATUS = False
IMG_1 = 0
IMG_2 = 0
IMG_3 = 0
CAM_POS = [0, 0]
P1 = [0, 0]

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/addtocart/')
def add_to_cart():
    global CAM_POS, P1
    render_template('addtocart.html')
    d, a = get_angle_length([500,200], [312, 500], [100,100])
    socketio.emit("commands", (d, a))




@app.route('/run_imgMatch/')
def image_match():
    socketio.emit('request img', 'request images from PI')
    # run_app()
    return "Image process done"


@app.route('/pi_send_img/')
def pi_connect():
    global PI_STATUS
    PI_STATUS = True
    return "pi connected!"


@app.route('/pi_status_connected/')
def pi_status_t():
    global PI_STATUS
    PI_STATUS = True


@app.route('/pi_status_disconnected/')
def pi_status_f():
    global PI_STATUS
    PI_STATUS = False


@socketio.on('This is test in main function')
def show_message(data):
    socketio.emit('request img', 'I\'m server, I want a image from you!')
    print('received message: ' + data)


@socketio.on('img_data_1')
def receive_img(data):
    global IMG_1
    data_1_decoded = base64.b64decode(data)
    IMG_1 = np.frombuffer(data_1_decoded, dtype=np.uint8)
    # ---------old method works on local but not on heroku-------
    # with open('image_1.png', 'wb') as f:
    #     f.write(base64.decodebytes(data))
    print('Image 1 received')
    # socketio.emit('receive finished')
    # -----------------------------------------------------------


@socketio.on('img_data_2')
def receive_img(data):
    global IMG_2
    data_2_decoded = base64.b64decode(data)
    IMG_2 = np.frombuffer(data_2_decoded, dtype=np.uint8)
    print('Image 2 received')


@socketio.on('img_data_3')
def receive_img(data):
    global IMG_1, IMG_2, IMG_3, CAM_POS, P1
    data_3_decoded = base64.b64decode(data)
    IMG_3 = np.frombuffer(data_3_decoded, dtype=np.uint8)
    print('Image 3 received')
    CAM_POS, P1 = run_app(IMG_1, IMG_2, IMG_3)
    print("Camera position: ", CAM_POS)
    print("P1: ", P1)









if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    server = pywsgi.WSGIServer(('127.0.0.1', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
    # socketio.run(app)
