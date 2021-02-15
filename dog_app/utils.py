import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


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
        os.remove(os.path.join(upload_folder, f))