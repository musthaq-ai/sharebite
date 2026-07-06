from flask import (
    Blueprint,
    session,
    redirect,
    url_for,
    render_template,
    request,
    flash
)

from models.user import User
from controllers.kyc_controller import upload_kyc

kyc = Blueprint(
    "kyc",
    __name__,
    url_prefix="/kyc"
)


# ==========================================
# UPLOAD KYC
# ==========================================

@kyc.route("/upload", methods=["GET", "POST"])
def upload():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = User.query.get(session["user_id"])

    if request.method == "POST":

        document = request.files.get("document")

        if document is None or document.filename == "":

            flash(
                "Please choose a document.",
                "danger"
            )

            return redirect(
                url_for("kyc.upload")
            )

        success = upload_kyc(
            user,
            document
        )

        if success:

            flash(
                "KYC uploaded successfully.",
                "success"
            )

        else:

            flash(
                "You have already uploaded your KYC. Please wait for admin verification.",
                "warning"
            )

        return redirect(
            url_for("kyc.upload")
        )

    return render_template(
        "kyc/upload.html",
        user=user
    )