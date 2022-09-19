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
    # global CAM_POS, P1
    # d_1, a_1 = get_angle_length(CAM_POS, [940, 480], P1)
    # d_2, a_2 = get_angle_length(CAM_POS, [180, 360], P1)
    # print("distance_1: ", d_1)
    # print("angle_1: ", a_1)
    # print("distance_2: ", d_2)
    # print("angle_2: ", a_2)
    # socketio.emit("receive_data", d_1)
    # socketio.emit("receive_data", a_1)
    # socketio.emit("receive_data", d_2)
    # socketio.emit("receive_data", a_2)
    socketio.emit("data_sent", "Run")
    return render_template('addtocart.html')


@app.route('/checkout/')
def close_sys():
    # d, a = get_angle_length(CAM_POS, [1500, 650], P1)
    # print("d_checkout", d)
    # print("a_checkout", a)
    # socketio.emit("receive_data", d)
    # socketio.emit("receive_data", a)
    socketio.emit("shut_down", "shut down script")
    return render_template('checkout.html')


@socketio.on('This is test in main function')
def show_message(data):
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
