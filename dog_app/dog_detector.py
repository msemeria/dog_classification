import json
import os

from torchvision import models

from .transform import transform_image

basedir = os.path.abspath(os.path.dirname(__file__))
imagenet_class_index = json.load(open(os.path.join(basedir, '_static/imagenet_class_index.json')))

vgg16 = models.vgg16(pretrained=True)
vgg16.eval()


def get_vgg16_prediction(img_path):
    """
        Return model inference on input image
    """
    # img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    input_img = transform_image(img_path)

    # Predict image's class
    prediction = vgg16(input_img)
    prediction = prediction.cpu()
    prediction = prediction.data.numpy().argmax()
    class_id, class_name = imagenet_class_index[str(prediction)]
    return prediction, class_name.replace("_", " ")


def dog_detector(img_path):
    """
        Return True if a dog is detected in the image stored at img_path
    """
    class_index, class_name = get_vgg16_prediction(img_path)
    return 151 <= class_index <= 268