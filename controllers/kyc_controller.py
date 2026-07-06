from helpers.file_helper import (
    save_uploaded_file,
    delete_uploaded_file
)

from models import db
from models.kyc import KYC


# ==========================================
# UPLOAD KYC
# ==========================================

def upload_kyc(user, file):

    existing = KYC.query.filter_by(
        user_id=user.id
    ).first()

    # -----------------------------
    # First Upload
    # -----------------------------

    if existing is None:

        filename = save_uploaded_file(
            file,
            "kyc"
        )

        kyc = KYC(

            user_type=user.role,

            user_id=user.id,

            document_name=file.filename,

            document_path="kyc/" + filename,

            status="Pending",

            reupload_allowed=False

        )

        db.session.add(kyc)

        user.kyc_status = "Pending"

        db.session.commit()

        return True

    # -----------------------------
    # Already Uploaded
    # -----------------------------

    if existing.reupload_allowed == "No":

        return False

    # -----------------------------
    # Re-upload Allowed
    # -----------------------------

    delete_uploaded_file(
        existing.document_path.replace("kyc/", ""),
        "kyc"
    )

    filename = save_uploaded_file(
        file,
        "kyc"
    )

    existing.document_name = file.filename

    existing.document_path = "kyc/" + filename

    existing.status = "Pending"

    existing.reupload_allowed = "No"

    existing.rejection_reason = None

    user.kyc_status = "Pending"

    db.session.commit()

    return True