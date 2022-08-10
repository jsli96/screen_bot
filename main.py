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
def pi_status():
    global PI_STATUS
    PI_STATUS = True


@app.route('/pi_status_disconnected/')
def pi_status():
    global PI_STATUS
    PI_STATUS = False


@socketio.on('This is test in main function')
def show_message(data):
    socketio.emit('request img', 'I\'m server, I want a image from you!')
    print('received message: ' + data)


@socketio.on('img_data')
def receive_img(data):
    with open('images/image_on_server.png', 'wb') as f:
        f.write(base64.decodebytes(data))
    print('Finished')
    socketio.emit('receive finished')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    server = pywsgi.WSGIServer(('127.0.0.1', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
    # socketio.run(app)
