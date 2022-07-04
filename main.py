from flask import Flask
# import numpy as np
# import cv2 as cv
# import timeit
# import imageMatch
app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World<"


if __name__ == '__main__':
    app.run()


