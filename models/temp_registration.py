from . import db
from datetime import datetime


class TempRegistration(db.Model):

    __tablename__ = "temp_registrations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Basic Details
    name = db.Column(
        db.String(150),
        nullable=False
    )

    organization_name = db.Column(
        db.String(200)
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(20),
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    address_line1 = db.Column(
        db.Text
    )

    address_line2 = db.Column(
        db.Text
    )

    district = db.Column(
        db.String(100)
    )

    state = db.Column(
        db.String(100)
    )

    role = db.Column(
        db.String(20),
        nullable=False
    )

    # OTP

    otp = db.Column(
        db.String(6),
        nullable=False
    )

    otp_created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    attempts = db.Column(
        db.Integer,
        default=0
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )