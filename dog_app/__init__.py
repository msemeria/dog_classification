import os

from flask import Flask, render_template, request, redirect, url_for
from flask_dropzone import Dropzone

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'uploads'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=1,
    # DROPZONE_REDIRECT_VIEW='result'
)

dropzone = Dropzone(app)


@app.route('/result/<img>', methods=['POST', 'GET'], )
def result(img):
    return render_template('result.html')


@app.route('/', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        file_path = os.path.join(app.config['UPLOADED_PATH'], f.filename)
        f.save(file_path)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
