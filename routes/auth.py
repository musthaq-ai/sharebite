from controllers.kyc_controller import upload_kyc
from flask import Blueprint, render_template, request, redirect, session, url_for
import bcrypt

from flask import flash

from models import db
from models.user import User

auth = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


# -----------------------------
# DONOR REGISTRATION
# -----------------------------
@auth.route("/donor-register", methods=["GET", "POST"])
def donor_register():

    if request.method == "POST":

        # Check if email already exists
        existing_email = User.query.filter_by(
            email=request.form["email"]
        ).first()

        if existing_email:

            flash(
        "Email already registered.",
        "danger"
    )

            return redirect(
        url_for("auth.donor_register")
    )

        # Check if phone already exists
        existing_phone = User.query.filter_by(
            phone=request.form["phone"]
        ).first()

        if existing_phone:

            flash(
        "Phone number already registered.",
        "danger"
            )

            return redirect(
        url_for("auth.donor_register")
    )

        # Hash password
        password = request.form["password"]

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        # Create user
        user = User(
            name=request.form["name"],
            organization_name=request.form["hotel_name"],
            email=request.form["email"],
            phone=request.form["phone"],
            password=hashed_password,
            address_line1=request.form["address1"],
            address_line2=request.form["address2"],
            district=request.form["district"],
            state=request.form["state"],
            latitude=0,
            longitude=0,
            role="Donor"
        )

        db.session.add(user)
        db.session.commit()

        flash(
    "Registration successful. Please login.",
    "success"
)

        return redirect(
    url_for("auth.login")
)

    return render_template("auth/donor_register.html")

# -----------------------------
# NGO REGISTRATION
# -----------------------------
@auth.route("/ngo-register", methods=["GET", "POST"])
def ngo_register():

    if request.method == "POST":

        # Check email
        existing_email = User.query.filter_by(
            email=request.form["email"]
        ).first()

        if existing_email:

            flash(
                "Email already registered.",
                "danger"
            )

            return redirect(url_for("auth.ngo_register"))

        # Check phone
        existing_phone = User.query.filter_by(
            phone=request.form["phone"]
        ).first()

        if existing_phone:

            flash(
                "Phone number already registered.",
                "danger"
            )

            return redirect(url_for("auth.ngo_register"))

        # Hash Password
        password = request.form["password"]

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        # Create NGO User
        ngo = User(

            name=request.form["name"],

            organization_name=request.form["organization_name"],

            email=request.form["email"],

            phone=request.form["phone"],

            password=hashed_password,

            address_line1=request.form["address1"],

            address_line2=request.form["address2"],

            district=request.form["district"],

            state=request.form["state"],

            latitude=0,

            longitude=0,

            role="NGO",

            kyc_status="Pending"

        )

        db.session.add(ngo)
        db.session.commit()

        # ======================================
        # Upload KYC Immediately
        # ======================================

        document = request.files.get("kyc_document")

        if document and document.filename != "":

            upload_kyc(
                ngo,
                document
            )

        flash(

            "Registration successful! Your KYC has been submitted for verification. Please wait for admin approval before logging in.",

            "success"

        )

        return redirect(url_for("auth.login"))

    return render_template("auth/ngo_register.html")
# -----------------------------
# LOGIN
# -----------------------------
@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        # ======================================
        # Find User
        # ======================================

        user = User.query.filter_by(
            email=email
        ).first()

        if user is None:

            flash(
                "Email not found.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )

        # ======================================
        # Verify Password
        # ======================================

        if not bcrypt.checkpw(

            password.encode("utf-8"),

            user.password.encode("utf-8")

        ):

            flash(
                "Incorrect password.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )

        # ======================================
        # Login Successful
        # ======================================

        session["user_id"] = user.id
        session["user_name"] = user.name
        session["role"] = user.role

        # ======================================
        # NGO KYC Verification
        # ======================================

        if user.role == "NGO":

            if user.kyc_status == "Pending":

                return redirect(
                    url_for("kyc.pending")
                )

            elif user.kyc_status == "Rejected":

                return redirect(
                    url_for("kyc.reupload")
                )

            elif user.kyc_status == "Approved":

                return redirect(
                    url_for("ngo.dashboard")
                )

        # ======================================
        # Donor Dashboard
        # ======================================

        elif user.role == "Donor":

            return redirect(
                url_for("donor.dashboard")
            )

        # ======================================
        # Admin Dashboard
        # ======================================

        elif user.role == "Admin":

            return redirect(
                url_for("admin.dashboard")
            )

    return render_template(
        "auth/login.html"
    )

#logout

@auth.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("auth.login"))