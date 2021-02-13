## Overview
This is a fork of Udacity's deep learning dog classification project. Original repository can be found at: https://github.com/udacity/deep-learning-v2-pytorch.git

This repository includes:
 - A jupyter notebook model/dog_app.ipynb and its associated files used to develop and train 2 deep learning models for dog breed classification. Refer to model/README.md for further instructions.
 - A simple web app using Flask in dog_app/
 
 ## Install
 ```
pip install -r requirements
```

## Run web app
In root dir:
 ```
export FLASK_APP=dog_app
export FLASK_ENV=development
flask run
```
The web app looks for a saved model file model/model_webapp.pt. This file can be obtained by executing model/dog_app.ipynb. If the file acnnot be found, the webapp defaults to using a Vgg16 pretrained model.