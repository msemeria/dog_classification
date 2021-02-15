import os

from flask import Flask, flash, request, redirect, send_from_directory, render_template
from werkzeug.utils import secure_filename

from .face_detector import face_detector
from .dog_detector import dog_detector
from .model_transfer import get_prediction
from .utils import allowed_file, delete_uploads

basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(basedir, 'uploads')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024


@app.route('/')
def index():
    """
        Display main page
    """
    return render_template('index.html')


@app.route('/', methods=['POST'])
def predict():
    """
        Upload a file to upload folder
    """
    delete_uploads(app.config['UPLOAD_FOLDER'])
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        class_index, class_name = get_prediction(filepath)
        # a dog is detected
        if dog_detector(filepath):
            return render_template('predict_dog.html', file=filename, prediction=class_name)
        # a human is detected
        elif face_detector(filepath):
            return render_template('predict_human.html', file=filename, prediction=class_name)
        else:
            return render_template('no_prediction.html', file=filename)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
        Display uploaded file
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
