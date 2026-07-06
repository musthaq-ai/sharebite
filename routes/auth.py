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
            return "Email already registered!"

        # Check if phone already exists
        existing_phone = User.query.filter_by(
            phone=request.form["phone"]
        ).first()

        if existing_phone:
            return "Phone number already registered!"

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
            return "Email already registered!"

        # Check phone
        existing_phone = User.query.filter_by(
            phone=request.form["phone"]
        ).first()

        if existing_phone:
            return "Phone number already registered!"

        # Hash Password
        password = request.form["password"]

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

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

            role="NGO"

        )

        db.session.add(ngo)

        db.session.commit()

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

        # Find user by email
        user = User.query.filter_by(email=email).first()

        if user is None:

            flash(
        "Email not found.",
        "danger" )

            return redirect(
                url_for("auth.login")
    )

        # Compare hashed password
        if bcrypt.checkpw(password.encode("utf-8"),user.password.encode("utf-8")):

            session["user_id"] = user.id
            session["user_name"] = user.name
            session["role"] = user.role

            if user.role == "Donor":
                return redirect(url_for("donor.dashboard"))

            elif user.role == "NGO":
                return redirect(url_for("ngo.dashboard"))

            elif user.role == "Admin":
                return redirect(url_for("admin.dashboard"))

        flash(
    "Incorrect password.",
    "danger"
)

        return redirect(
    url_for("auth.login")
)

    return render_template("auth/login.html")

#logout

@auth.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("auth.login"))