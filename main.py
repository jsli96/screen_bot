from flask import Flask, render_template
# import numpy as np
# import cv2 as cv
# import timeit
# import imageMatch
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_imgMatch')
def b_test():
    print("Hello")
    print("running image Match")
    return ()


if __name__ == '__main__':
    app.run()


