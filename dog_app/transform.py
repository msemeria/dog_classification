import torch
from PIL import Image
from torchvision.transforms import transforms


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
