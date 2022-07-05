from flask import Flask, render_template
from imageMatch import *
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/run_imgMatch')
def image_match():
    run_app()
    return "Image process done"


if __name__ == '__main__':
    app.run()


