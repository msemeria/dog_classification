import cv2
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# extract pre-trained face detector
face_cascade = cv2.CascadeClassifier(os.path.join(basedir, '../model/haarcascades/haarcascade_frontalface_alt.xml'))


def face_detector(img_path):
    """
        Return True if face is detected in image stored at img_path
    """
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)
    return len(faces) > 0
