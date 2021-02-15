import os
import torch

from torchvision import models

from .transform import transform_image

basedir = os.path.abspath(os.path.dirname(__file__))

transfer_model_class_index_file = open(os.path.join(basedir, '_static/class_names_transfer.txt'), 'r')
transfer_model_class_index = transfer_model_class_index_file.readlines()

model = models.vgg16(pretrained=True)
model_state_dict = os.path.join(basedir, '../model/model_transfer.pt')
# replace classifier
model.classifier[6] = torch.nn.Linear(4096, 133, bias=True)  # replace vgg16's last classifier
model.load_state_dict(torch.load(model_state_dict,  map_location=torch.device('cpu')))
for param in model.features.parameters():
    param.requires_grad = False
model.eval()  # Switch model to inference (evaluation) mode


def get_prediction(img_path):
    """
        Return model inference on input image
    """
    # img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    input_img = transform_image(img_path)

    # Predict image's class
    prediction = model(input_img)
    prediction = prediction.cpu()
    prediction = prediction.data.numpy().argmax()
    class_name = transfer_model_class_index[prediction]
    print(prediction, class_name)
    return prediction, class_name.replace("_", " ")