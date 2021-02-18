## Overview
This is a fork of Udacity's deep learning dog classification project. Original repository can be found at: https://github.com/udacity/deep-learning-v2-pytorch.git

This repository includes:
 - A simple web app that predicts the dog breed of a dog in an uploaded picture in dog_app/
 - A jupyter notebook model/dog_app.ipynb and its associated files used to develop and train 2 deep learning models for dog breed classification. Refer to model/README.md for further instructions.
 - The project proposal document: proposal.pdf
 - The project report: report.pdf
 
 ## Install
 ```
pip install -r requirements
```
The web application looks for a model's state dictionary saved into a file model/model_transfer.pt. You can obtain this file by running the Jupyter notebook model/dog_app.ipynb, or download it [here](https://msemeria-s3-fr.s3.eu-west-3.amazonaws.com/model_transfer.pt).

## Run web app
In project root dir:
 ```
export FLASK_APP=dog_app
export FLASK_ENV=development
flask run
```

## Example
![](./example/example.png)
