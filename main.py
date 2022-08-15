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

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/run_imgMatch/')
def image_match():
    socketio.emit('request img', 'request images from PI')
    run_app()
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
    IMG_1 = np.fromstring(data, dtype=np.uint8)
    # ---------old method works on local but not on heroku-------
    # with open('image_1.png', 'wb') as f:
    #     f.write(base64.decodebytes(data))
    print('Finished')
    # socketio.emit('receive finished')
    # -----------------------------------------------------------


@socketio.on('img_data_2')
def receive_img(data):
    global IMG_2
    IMG_2 = np.fromstring(data, dtype=np.uint8)
    print('Finished')

@socketio.on('img_data_3')
def receive_img(data):
    global IMG_3
    IMG_3 = np.fromstring(data, dtype=np.uint8)
    print('Finished')
    run_app(IMG_1, IMG_2, IMG_3)



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    server = pywsgi.WSGIServer(('127.0.0.1', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
    # socketio.run(app)
