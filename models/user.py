from . import db

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    organization_name = db.Column(db.String(150), nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)

    phone = db.Column(db.String(15), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    address_line1 = db.Column(db.String(255), nullable=False)

    address_line2 = db.Column(db.String(255))

    district = db.Column(db.String(100), nullable=False)

    state = db.Column(db.String(100), nullable=False)

    latitude = db.Column(db.Numeric(10,8), nullable=False)

    longitude = db.Column(db.Numeric(11,8), nullable=False)

    role = db.Column(
    db.Enum(
        'Donor',
        'NGO',
        'Admin',
        name="user_role_enum"
    ),
    nullable=False,
    default='Donor'
)
    email_verified = db.Column(db.Boolean, default=False)

    kyc_status = db.Column(
    db.Enum(
        'Pending',
        'Approved',
        'Rejected',
        name="kyc_status_enum"
    ),
    default='Pending'
)

    created_at = db.Column(db.DateTime)

    updated_at = db.Column(db.DateTime)