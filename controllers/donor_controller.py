import os
import uuid

from flask import jsonify

from flask import current_app
from werkzeug.utils import secure_filename

from models import db
from models import booking
from models import donation
from models.donation import FoodDonation

from sqlalchemy import or_

from sqlalchemy import func
from datetime import datetime, timedelta

from models.booking import Booking
from models.donation import FoodDonation

from utils.qr_generator import generate_booking_qr

from controllers.notification_controller import create_notification

# =====================================================
# DASHBOARD
# =====================================================
def get_dashboard_data(donor_id):

    # ===============================
    # Statistics
    # ===============================

    total_donations = FoodDonation.query.filter_by(
        donor_id=donor_id
    ).count()

    available_food = FoodDonation.query.filter_by(
        donor_id=donor_id,
        status="Available"
    ).count()

    booked_food = FoodDonation.query.filter_by(
        donor_id=donor_id,
        status="Booked"
    ).count()

    completed_food = FoodDonation.query.filter_by(
        donor_id=donor_id,
        status="Completed"
    ).count()

    # ===============================
    # Recent Donations
    # ===============================

    recent_donations = (

        FoodDonation.query

        .filter_by(donor_id=donor_id)

        .order_by(FoodDonation.id.desc())

        .limit(5)

        .all()

    )

    # ===============================
    # Weekly Chart
    # ===============================

    weekly_labels = []

    weekly_counts = []

    today = datetime.now().date()

    for i in range(6, -1, -1):

        day = today - timedelta(days=i)

        weekly_labels.append(day.strftime("%a"))

        count = FoodDonation.query.filter(

            FoodDonation.donor_id == donor_id,

            func.date(FoodDonation.prepared_time) == day

        ).count()

        weekly_counts.append(count)

    # ===============================
    # Doughnut Chart
    # ===============================

    status_counts = [

        available_food,

        booked_food,

        completed_food

    ]

    return {

        "total_donations": total_donations,

        "available_food": available_food,

        "booked_food": booked_food,

        "completed_food": completed_food,

        "recent_donations": recent_donations,

        "weekly_labels": weekly_labels,

        "weekly_counts": weekly_counts,

        "status_counts": status_counts

    }

# =====================================================
# MY DONATIONS
# =====================================================

def get_my_donations(donor_id, search=None, status=None):

    query = FoodDonation.query.filter_by(
        donor_id=donor_id
    )

    if search:

        query = query.filter(
            FoodDonation.food_name.ilike(f"%{search}%")
        )

    if status and status != "All":

        query = query.filter_by(
            status=status
        )

    return (
        query
        .order_by(FoodDonation.id.desc())
        .all()
    )

# =====================================================
# SAVE FOOD
# =====================================================

def save_food(form, files, donor_id):

    filename = ""

    image = files.get("image")

    if image and image.filename != "":

        extension = os.path.splitext(image.filename)[1]

        filename = secure_filename(
            f"{uuid.uuid4().hex}{extension}"
        )

        food_folder = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            "food"
        )

        os.makedirs(food_folder, exist_ok=True)

        image.save(
            os.path.join(
                food_folder,
                filename
            )
        )

    donation = FoodDonation(

        donor_id=donor_id,

       food_name=form.getlist("food_name[]")[0],

quantity=form.getlist("quantity[]")[0],

category=form.getlist("category[]")[0],

veg_nonveg=form.getlist("veg_nonveg[]")[0],

        prepared_time=form["prepared_time"],

        expiry_time=form["expiry_time"],

        description=form.getlist("description[]")[0],

        image=filename,

        pickup_address=form["pickup_address"],

        latitude=form["latitude"],

        longitude=form["longitude"],

        status="Available"

    )

    db.session.add(donation)
    db.session.commit()

# =====================================================
# GET SINGLE DONATION
# =====================================================

def get_donation_by_id(donation_id, donor_id):

    return FoodDonation.query.filter_by(
        id=donation_id,
        donor_id=donor_id
    ).first()

# =====================================================
# UPDATE DONATION
# =====================================================

def update_donation(donation, form, files):

    # Food Details
    donation.food_name = form.getlist("food_name[]")[0]
    donation.quantity = form.getlist("quantity[]")[0]
    donation.category = form.getlist("category[]")[0]
    donation.veg_nonveg = form.getlist("veg_nonveg[]")[0]
    donation.description = form.getlist("description[]")[0]

    # Other Details
    donation.prepared_time = form.get("prepared_time")
    donation.expiry_time = form.get("expiry_time")
    donation.pickup_address = form.get("pickup_address")
    donation.latitude = form.get("latitude")
    donation.longitude = form.get("longitude")

    # Upload New Image (if selected)
    image = files.get("image")

    if image and image.filename:

        extension = os.path.splitext(image.filename)[1]

        filename = secure_filename(
            f"{uuid.uuid4().hex}{extension}"
        )

        food_folder = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            "food"
        )

        os.makedirs(food_folder, exist_ok=True)

        image.save(
            os.path.join(food_folder, filename)
        )

        donation.image = filename

    db.session.commit()
# =====================================================
# DELETE DONATION
# =====================================================

def delete_donation(donation):

    if donation.image:

        image_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            "food",
            donation.image
        )

        if os.path.exists(image_path):

            os.remove(image_path)

    db.session.delete(donation)
    db.session.commit()
# =====================================================
# GET BOOKING REQUESTS
# =====================================================

def get_booking_requests(donor_id):

    requests = (
        Booking.query
        .join(FoodDonation)
        .filter(
            FoodDonation.donor_id == donor_id
        )
        .order_by(
            Booking.booking_time.desc()
        )
        .all()
    )

    return requests
# -----------------------------------
# ACCEPT BOOKING
# -----------------------------------

# -----------------------------------
# ACCEPT BOOKING
# -----------------------------------
def accept_booking(booking_id, donor_id):

    booking = (
        Booking.query
        .join(FoodDonation)
        .filter(
            Booking.id == booking_id,
            FoodDonation.donor_id == donor_id
        )
        .first()
    )

    if booking is None:
        return False

    # Prevent accepting twice
    if booking.booking_status == "Accepted":
        return True

    booking.booking_status = "Accepted"

    booking.food.status = "Booked"

    # ==========================
    # Generate QR Token
    # ==========================

    booking.qr_token = uuid.uuid4().hex

    booking.qr_generated_at = datetime.utcnow()

    booking.qr_verified = False

    booking.verified_at = None

# Save first to ensure booking.id exists
    db.session.commit()

# Generate QR image
    booking.qr_image = generate_booking_qr(booking)

    db.session.commit()

    # ==========================
    # Notify NGO
    # ==========================

    create_notification(

        receiver_type="NGO",

        receiver_id=booking.ngo_id,

        title="Booking Accepted",

        message=f"Your booking for '{booking.food.food_name}' has been accepted. Your pickup QR Code is now available."

    )

    return True
# -----------------------------------
# REJECT BOOKING
# -----------------------------------

def reject_booking(booking_id, donor_id):

    booking = (
        Booking.query
        .join(FoodDonation)
        .filter(
            Booking.id == booking_id,
            FoodDonation.donor_id == donor_id
        )
        .first()
    )

    if booking is None:
        return False

    booking.booking_status = "Rejected"

    booking.food.status = "Available"

    db.session.commit()

    # Notify NGO
    create_notification(

        receiver_type="NGO",

        receiver_id=booking.ngo_id,

        title="Booking Rejected",

        message=f"Your booking for '{booking.food.food_name}' was rejected."

    )

    return True
# -----------------------------------
# COMPLETE DONATION
# -----------------------------------


# -----------------------------------
# COMPLETE DONATION
# -----------------------------------

def complete_donation(booking_id, donor_id):

    booking = (
        Booking.query
        .join(FoodDonation)
        .filter(
            Booking.id == booking_id,
            FoodDonation.donor_id == donor_id
        )
        .first()
    )

    if booking is None:
        return False

    booking.booking_status = "Completed"

    booking.completed_time = datetime.now()

    booking.food.status = "Completed"

    db.session.commit()

    # Notify NGO
    create_notification(

        receiver_type="NGO",

        receiver_id=booking.ngo_id,

        title="Donation Completed",

        message=f"The donation '{booking.food.food_name}' has been marked as completed."

    )

    return True
def verify_qr(data, donor_id):

    booking = db.session.get(Booking, int(data["booking_id"]))

    if booking is None:

        return {

            "success": False,

            "message": "Booking not found."

        }

    if booking.food.donor_id != donor_id:

        return {

            "success": False,

            "message": "This booking doesn't belong to you."

        }
    if booking.booking_status != "Accepted":

        return {

        "success": False,

        "message": f"Booking is {booking.booking_status}. QR verification is not allowed."

    }

    if booking.qr_verified:

        return {

            "success": False,

            "message": "QR Code already used."

        }

    if booking.qr_token != data["token"]:

        return {

            "success": False,

            "message": "Invalid QR Code."

        }

    booking.qr_verified = True

    booking.verified_at = datetime.utcnow()

    booking.booking_status = "Picked Up"

    booking.food.status = "Picked Up"

    db.session.commit()

    return {

    "success": True,

    "booking_id": booking.id,

    "food_name": booking.food.food_name,

    "ngo_name": booking.ngo.organization_name,

    "message": "NGO verified successfully. Food can now be handed over."

}

def verify_booking_qr(qr_data):

    try:

        booking_id, qr_token = qr_data.split("|")

    except ValueError:

        return jsonify({

            "success": False,

            "message": "Invalid QR Code"

        })

    booking = Booking.query.filter_by(

        id=int(booking_id),

        qr_token=qr_token

    ).first()

    if booking is None:

        return jsonify({

            "success": False,

            "message": "QR Code not found."

        })

    if booking.qr_verified:

        return jsonify({

            "success": False,

            "message": "This QR has already been scanned."

        })

    booking.qr_verified = True

    booking.booking_status = "Completed"

    booking.completed_time = datetime.utcnow()

    booking.verified_at = datetime.utcnow()

    booking.food.status = "Completed"

    db.session.commit()

    return jsonify({

        "success": True,

        "message": "Food handover completed successfully."

    })