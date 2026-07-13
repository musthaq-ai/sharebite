from datetime import datetime

from models import db
from models.temp_registration import TempRegistration
from models.user import User

from helpers.email_helper import (
    generate_otp,
    send_otp_email
)
import bcrypt
from datetime import datetime, timedelta

from models.user import User


def create_temp_registration(data):

    print("STEP 1: Function called")

    existing = TempRegistration.query.filter_by(
        email=data["email"]
    ).first()

    if existing:
        print("STEP 2: Existing record found, deleting...")
        db.session.delete(existing)
        db.session.commit()

    otp = generate_otp()
    print("STEP 3: OTP =", otp)

    temp = TempRegistration(
        name=data["name"],
        organization_name=data["organization_name"],
        email=data["email"],
        phone=data["phone"],
        password=data["password"],
        address_line1=data["address1"],
        address_line2=data["address2"],
        district=data["district"],
        state=data["state"],
        role=data["role"],
        otp=otp,
        otp_created_at=datetime.utcnow()
    )

    print("STEP 4: Temp object created")

    db.session.add(temp)

    print("STEP 5: Added to session")

    db.session.commit()

    print("STEP 6: Commit successful")

    send_otp_email(temp.email, otp)

    print("STEP 7: Email sent")

    return temp
# ==========================================
# VERIFY OTP
# ==========================================

def verify_registration_otp(temp_id, entered_otp):

    temp = TempRegistration.query.get(temp_id)

    if temp is None:

        return False, "Registration session expired."

    # OTP expires in 5 minutes
    if datetime.utcnow() > temp.otp_created_at + timedelta(minutes=5):

        db.session.delete(temp)
        db.session.commit()

        return False, "OTP has expired. Please register again."

    if temp.otp != entered_otp:

        return False, "Invalid OTP."

    # Create actual user

    user = User(

        name=temp.name,

        organization_name=temp.organization_name,

        email=temp.email,

        phone=temp.phone,

        password=temp.password,

        address_line1=temp.address_line1,

        address_line2=temp.address_line2,

        district=temp.district,

        state=temp.state,

        latitude=0,

        longitude=0,

        role=temp.role,

        kyc_status="Pending" if temp.role == "NGO" else "Approved"

    )

    db.session.add(user)

    db.session.commit()

    # Delete temporary registration

    db.session.delete(temp)

    db.session.commit()

    return True, "Registration successful."
# ==========================================
# RESEND OTP
# ==========================================

def resend_registration_otp(temp_id):

    temp = TempRegistration.query.get(temp_id)

    if temp is None:

        return False

    otp = generate_otp()

    temp.otp = otp

    temp.otp_created_at = datetime.utcnow()

    db.session.commit()

    send_otp_email(

        temp.email,

        otp

    )

    return True