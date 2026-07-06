import os
import uuid

from flask import current_app
from werkzeug.utils import secure_filename


# ==========================================
# SAVE FILE
# ==========================================

def save_uploaded_file(file, folder):

    if file is None or file.filename == "":
        return ""

    extension = os.path.splitext(file.filename)[1]

    filename = secure_filename(
        f"{uuid.uuid4().hex}{extension}"
    )

    upload_folder = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        folder
    )

    os.makedirs(
        upload_folder,
        exist_ok=True
    )

    file.save(
        os.path.join(
            upload_folder,
            filename
        )
    )

    return filename


# ==========================================
# DELETE FILE
# ==========================================

def delete_uploaded_file(filename, folder):

    if not filename:
        return

    path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        folder,
        filename
    )

    if os.path.exists(path):

        os.remove(path)