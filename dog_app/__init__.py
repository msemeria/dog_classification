import json
import os

import torch

from PIL import Image
from flask import Flask, flash, request, redirect, send_from_directory, render_template
from torchvision import models
from torchvision.transforms import transforms
from werkzeug.utils import secure_filename

basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024

imagenet_class_index = json.load(open(os.path.join(basedir, '_static/imagenet_class_index.json')))

custom_model = os.path.join(basedir, '../model/model_webapp.pt')
if os.path.exists(custom_model):
    model = torch.load(custom_model, map_location=torch.device('cpu'))
else:
    model = models.vgg16(pretrained=True)
    print("No custom model found, defaulting to vgg16")
model.eval()  # Switch model to inference (evaluation) mode


def allowed_file(filename):
    """
        Validate file extension
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def delete_uploads(upload_folder):
    """
        Remove all uploaded files in upload folder
    """
    files = os.listdir(upload_folder)
    for f in files:
        os.remove(os.path.join(UPLOAD_FOLDER, f))


def transform_image(img_path):
    """
        Preprocess image to fit model's input format
    """
    # load the image and return the predicted breed
    # Load image
    img = Image.open(img_path)

    # Define the pre-processing steps that will be applied to the image
    transform = transforms.Compose([
        transforms.Resize(400),  # Resize the image to 256x256 pixels
        transforms.CenterCrop(224),  # Keep a 224x224 zone around the center
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],  # Normalize using values advised in pytorch documentation
                             std=[0.229, 0.224, 0.225]),
    ])

    # Pre-process the image
    preprocessed_img = transform(img)

    # if use_cuda:
    #     preprocessed_img = preprocessed_img.to('cuda')

    return torch.unsqueeze(preprocessed_img, 0)  # add a "batch" dimension to fit expected input format


def get_prediction(filename):
    """
        Return model inference on input image
    """
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    input_img = transform_image(img_path)

    # Predict image's class
    prediction = model(input_img)
    prediction = prediction.cpu()
    prediction = prediction.data.numpy().argmax()
    class_id, class_name = imagenet_class_index[str(prediction)]
    print(prediction, class_name)
    return class_name.replace("_", " ")


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
        prediction = get_prediction(filepath)
        return render_template('predict.html', file=filename, prediction=prediction)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
        Display uploaded file
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
