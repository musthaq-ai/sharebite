# ==========================================
# VALIDATE IMAGE
# ==========================================

ALLOWED_IMAGE_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png"
}


def allowed_image(filename):

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_IMAGE_EXTENSIONS


# ==========================================
# VALIDATE DOCUMENT
# ==========================================

ALLOWED_DOCUMENT_EXTENSIONS = {
    "pdf",
    "jpg",
    "jpeg",
    "png"
}


def allowed_document(filename):

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_DOCUMENT_EXTENSIONS