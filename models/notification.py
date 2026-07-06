from models import db


class Notification(db.Model):

    __tablename__ = "notifications"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    receiver_type = db.Column(
    db.Enum(
        "Donor",
        "NGO",
        "Admin",
        name="receiver_type_enum"
    ),
    nullable=False
)

    receiver_id = db.Column(
        db.Integer,
        nullable=False
    )

    title = db.Column(
        db.String(255),
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

    status = db.Column(
    db.Enum(
        "Unread",
        "Read",
        name="notification_status_enum"
    ),
    default="Unread"
)

    created_at = db.Column(
        db.DateTime
    )