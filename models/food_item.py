from . import db


class FoodItem(db.Model):

    __tablename__ = "food_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    donation_id = db.Column(
        db.Integer,
        db.ForeignKey("food_donations.id"),
        nullable=False
    )

    food_name = db.Column(
        db.String(150),
        nullable=False
    )

    quantity = db.Column(
        db.String(100),
        nullable=False
    )

    category = db.Column(
        db.String(50),
        nullable=False
    )

    veg_nonveg = db.Column(
        db.String(20),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    donation = db.relationship(
        "FoodDonation",
        backref=db.backref(
            "food_items",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )