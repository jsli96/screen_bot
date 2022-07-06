from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import logging
from imageMatch import *


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


@app.route('/pi_status/')
def pi_status():
    global PI_STATUS
    if PI_STATUS is True:
        return "pi connected!"
    else:
        return "pi disconnected!"


@app.route('/testing/')
def socketio_test():
    msg = {'data': 'hello! This is in testing io'}
    socketio.emit('worker_msg', msg)


@socketio.on('This is test in main function')
def show_message(data):
    print('received message: ' + data)


if __name__ == '__main__':
    # app.run()
    logging.basicConfig(level=logging.DEBUG)
    server = pywsgi.WSGIServer(('127.0.0.1', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
    # socketio.run(app)
