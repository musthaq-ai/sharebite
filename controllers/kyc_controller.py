from helpers.file_helper import (
    save_uploaded_file,
    delete_uploaded_file
)

from models import db
from models.kyc import KYC


# ==========================================
# UPLOAD / RE-UPLOAD KYC
# ==========================================

def upload_kyc(user, file):

    existing = KYC.query.filter_by(
        user_id=user.id
    ).first()

    # ==========================================
    # FIRST UPLOAD
    # ==========================================

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

            reupload_allowed=False,

            admin_remark=None

        )

        db.session.add(kyc)

        user.kyc_status = "Pending"

        db.session.commit()

        return True

    # ==========================================
    # RE-UPLOAD NOT ALLOWED
    # ==========================================

    if not existing.reupload_allowed:

        return False

    # ==========================================
    # RE-UPLOAD ALLOWED
    # ==========================================

    # Delete old document
    delete_uploaded_file(

        existing.document_path.replace("kyc/", ""),

        "kyc"

    )

    # Save new document
    filename = save_uploaded_file(

        file,

        "kyc"

    )

    existing.document_name = file.filename

    existing.document_path = "kyc/" + filename

    existing.status = "Pending"

    existing.reupload_allowed = False

    existing.admin_remark = None

    existing.verified_at = None

    user.kyc_status = "Pending"

    db.session.commit()

    return True