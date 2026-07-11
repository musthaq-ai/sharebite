import os
from models.user import User
from models.donation import FoodDonation
from models.booking import Booking
from models.user import User
from sqlalchemy import or_
from models import db
from models.booking import Booking
from flask import current_app
from datetime import datetime
from models.kyc import KYC

from controllers.notification_controller import create_notification

# ==========================================
# ADMIN DASHBOARD
# ==========================================

def get_dashboard_data():

    total_donors = User.query.filter_by(
        role="Donor"
    ).count()

    total_ngos = User.query.filter_by(
        role="NGO"
    ).count()

    total_donations = FoodDonation.query.count()

    total_bookings = Booking.query.count()

    completed_donations = FoodDonation.query.filter_by(
        status="Completed"
    ).count()

    recent_users = (
        User.query
        .order_by(User.id.desc())
        .limit(5)
        .all()
    )

    recent_donations = (
        FoodDonation.query
        .order_by(FoodDonation.id.desc())
        .limit(5)
        .all()
    )

    recent_bookings = (
        Booking.query
        .order_by(Booking.id.desc())
        .limit(5)
        .all()
    )
    # ==========================================
    # CHART DATA
    # ==========================================

    donation_status = [

        FoodDonation.query.filter_by(status="Available").count(),

        FoodDonation.query.filter_by(status="Booked").count(),

        FoodDonation.query.filter_by(status="Completed").count()

    ]

    booking_status = [

        Booking.query.filter_by(booking_status="Pending").count(),

        Booking.query.filter_by(booking_status="Accepted").count(),

        Booking.query.filter_by(booking_status="Picked Up").count(),

        Booking.query.filter_by(booking_status="Completed").count(),

        Booking.query.filter_by(booking_status="Rejected").count()

    ]

    user_distribution = [

        total_donors,

        total_ngos

    ]

    kyc_status = [

        User.query.filter_by(kyc_status="Pending").count(),

        User.query.filter_by(kyc_status="Approved").count(),

        User.query.filter_by(kyc_status="Rejected").count()

    ]
    return {

        "total_donors": total_donors,

        "total_ngos": total_ngos,

        "total_donations": total_donations,

        "total_bookings": total_bookings,

        "completed_donations": completed_donations,

        "recent_users": recent_users,

        "recent_donations": recent_donations,

        "recent_bookings": recent_bookings,
        "donation_status": donation_status,

        "booking_status": booking_status,

        "user_distribution": user_distribution,

        "kyc_status": kyc_status,

    }
    
# ==========================================
# GET ALL USERS
# ==========================================



def get_all_users(search=None, role=None):

    query = User.query

    if search:

        query = query.filter(

            or_(

                User.name.ilike(f"%{search}%"),

                User.email.ilike(f"%{search}%"),

                User.organization_name.ilike(f"%{search}%")

            )

        )

    if role and role != "All":

        query = query.filter_by(role=role)

    return (

        query

        .order_by(User.id.desc())

        .all()

    )

# ==========================================
# GET USER DETAILS
# ==========================================

def get_user_details(user_id):

    return User.query.get(user_id)
# ==========================================
# DELETE USER
# ==========================================

def delete_user(user_id):

    user = User.query.get(user_id)

    if user is None:

        return False

    # Prevent deleting admin accounts
    if user.role == "Admin":

        return False

    db.session.delete(user)

    db.session.commit()

    return True
# ==========================================
# GET ALL DONATIONS
# ==========================================

from models.donation import FoodDonation


def get_all_donations(search=None, status=None):

    query = FoodDonation.query

    if search:

        query = query.filter(

            FoodDonation.food_name.ilike(
                f"%{search}%"
            )

        )

    if status and status != "All":

        query = query.filter_by(
            status=status
        )

    return (

        query

        .order_by(
            FoodDonation.id.desc()
        )

        .all()

    )


# ==========================================
# DELETE DONATION
# ==========================================


def admin_delete_donation(donation_id):

    donation = FoodDonation.query.get(donation_id)

    if donation is None:

        return False

    # ----------------------------------
    # Delete all bookings of this donation
    # ----------------------------------

    Booking.query.filter_by(

        food_id=donation.id

    ).delete()

    # ----------------------------------
    # Delete uploaded food image
    # ----------------------------------

    if donation.image:

        image_path = os.path.join(

            current_app.config["UPLOAD_FOLDER"],

            "food",

            donation.image

        )

        if os.path.exists(image_path):

            os.remove(image_path)

    # ----------------------------------
    # Delete Donation
    # ----------------------------------

    db.session.delete(donation)

    db.session.commit()

    return True
# ==========================================
# GET ALL BOOKINGS
# ==========================================



def get_all_bookings(status=None):

    query = Booking.query

    if status and status != "All":

        query = query.filter_by(
            booking_status=status
        )

    return (
        query
        .order_by(Booking.booking_time.desc())
        .all()
    )
    
# =====================================================
# GET KYC REQUESTS
# =====================================================

def get_kyc_requests():

    return (
        KYC.query
        .order_by(KYC.id.desc())
        .all()
    )
# =====================================================
# APPROVE KYC
# =====================================================

def approve_kyc(kyc_id):

    kyc = KYC.query.get(kyc_id)

    if kyc is None:
        return False

    kyc.status = "Approved"
    kyc.reupload_allowed = False

    kyc.admin_remark = None
    kyc.verified_at = datetime.now()

    user = User.query.get(kyc.user_id)
    user.kyc_status = "Approved"

    db.session.commit()

    # Notify User
    create_notification(
        receiver_type=user.role,
        receiver_id=user.id,
        title="KYC Approved",
        message="Congratulations! Your KYC has been approved successfully."
    )

    return True
# =====================================================
# REJECT KYC
# =====================================================

def reject_kyc(kyc_id, reason):

    kyc = KYC.query.get(kyc_id)

    if kyc is None:
        return False

    kyc.status = "Rejected"
    kyc.admin_remark = reason
    kyc.reupload_allowed = True

    user = User.query.get(kyc.user_id)
    user.kyc_status = "Rejected"

    db.session.commit()

    # Notify User
    create_notification(
        receiver_type=user.role,
        receiver_id=user.id,
        title="KYC Rejected",
        message=f"Your KYC verification was rejected.\nReason: {reason}"
    )

    return True