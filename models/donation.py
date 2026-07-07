from . import db


class FoodDonation(db.Model):

    __tablename__ = "food_donations"

    id = db.Column(db.Integer, primary_key=True)

    donor_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    food_name = db.Column(db.String(150), nullable=False)

    quantity = db.Column(db.String(100), nullable=False)

    category = db.Column(db.String(100), nullable=False)

    veg_nonveg = db.Column(db.String(20), nullable=False)

    prepared_time = db.Column(db.DateTime)

    expiry_time = db.Column(db.DateTime)

    description = db.Column(db.Text)

    image = db.Column(db.String(255))

    pickup_address = db.Column(db.Text)
    area_name = db.Column(
    db.String(150)
)

    city = db.Column(
    db.String(150)
)

    state = db.Column(
    db.String(150)
)

    country = db.Column(
    db.String(150)
)

    latitude = db.Column(db.Numeric(10, 8))

    longitude = db.Column(db.Numeric(11, 8))

    status = db.Column(
        db.String(30),
        default="Available"
    )

    # Relationship with User (Donor)
    donor = db.relationship(
        "User",
        backref="donations"
    )