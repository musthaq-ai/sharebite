from . import db


class KYC(db.Model):

    __tablename__ = "kyc"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_type = db.Column(
        db.String(20),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    document_name = db.Column(
        db.String(255),
        nullable=False
    )

    document_path = db.Column(
        db.String(255),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )
    reupload_allowed = db.Column(
    db.Boolean,
    default=False
)

# NEW
    admin_remark = db.Column(
    db.Text
)

# NEW
    uploaded_at = db.Column(
    db.DateTime
)

    verified_at = db.Column(
        db.DateTime
    )

    user = db.relationship(
        "User",
        backref="kyc_documents"
    )