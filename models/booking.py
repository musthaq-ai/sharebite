from models import db


class Booking(db.Model):

    __tablename__ = "bookings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    food_id = db.Column(
        db.Integer,
        db.ForeignKey("food_donations.id"),
        nullable=False
    )

    ngo_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    booking_status = db.Column(
        db.String(20),
        default="Pending"
    )

    booking_time = db.Column(
        db.DateTime
    )

    pickup_time = db.Column(
        db.DateTime
    )

    completed_time = db.Column(
        db.DateTime
    )
    
# ==============================
# QR Verification
# ==============================

    qr_token = db.Column(
    db.String(64),
    unique=True
)

    qr_verified = db.Column(
    db.Boolean,
    default=False
)

    qr_generated_at = db.Column(
    db.DateTime
)
    qr_image = db.Column(
    db.String(255)
)

    verified_at = db.Column(
    db.DateTime
)
    # Relationships
    food = db.relationship(
        "FoodDonation",
        backref="bookings"
    )

    ngo = db.relationship(
        "User",
        backref="ngo_bookings"
    )