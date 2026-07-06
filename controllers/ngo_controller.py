from datetime import datetime

from models import db
from models.booking import Booking
from models.donation import FoodDonation

from controllers.notification_controller import create_notification


# ==========================================
# NGO DASHBOARD
# ==========================================

def get_dashboard_data(ngo_id):

    total_bookings = Booking.query.filter_by(
        ngo_id=ngo_id
    ).count()

    pending_bookings = Booking.query.filter_by(
        ngo_id=ngo_id,
        booking_status="Pending"
    ).count()

    accepted_bookings = Booking.query.filter_by(
        ngo_id=ngo_id,
        booking_status="Accepted"
    ).count()

    completed_bookings = Booking.query.filter_by(
        ngo_id=ngo_id,
        booking_status="Completed"
    ).count()

    available_food = FoodDonation.query.filter_by(
        status="Available"
    ).count()

    recent_bookings = (
        Booking.query
        .filter_by(ngo_id=ngo_id)
        .order_by(Booking.id.desc())
        .limit(5)
        .all()
    )

    return {

        "total_bookings": total_bookings,

        "pending_bookings": pending_bookings,

        "accepted_bookings": accepted_bookings,

        "completed_bookings": completed_bookings,

        "available_food": available_food,

        "recent_bookings": recent_bookings

    }


# ==========================================
# AVAILABLE FOOD
# ==========================================

def get_available_food():

    return (

        FoodDonation.query

        .filter_by(status="Available")

        .order_by(FoodDonation.id.desc())

        .all()

    )


# ==========================================
# GET FOOD DETAILS
# ==========================================

def get_food_by_id(food_id):

    return FoodDonation.query.get(food_id)


# ==========================================
# BOOK FOOD
# ==========================================

def book_food(food_id, ngo_id):

    donation = FoodDonation.query.get(food_id)

    if donation is None:
        return False

    if donation.status != "Available":
        return False

    booking = Booking(

        food_id=food_id,

        ngo_id=ngo_id,

        booking_status="Pending",

        booking_time=datetime.now()

    )

    db.session.add(booking)

    donation.status = "Pending"

    db.session.commit()

    # Notify Donor
    create_notification(

        receiver_type="Donor",

        receiver_id=donation.donor_id,

        title="New Booking Request",

        message=f"An NGO has requested '{donation.food_name}'. Please review the booking request."

    )

    return True


# ==========================================
# MY BOOKINGS
# ==========================================

def get_my_bookings(ngo_id):

    return (

        Booking.query

        .filter_by(ngo_id=ngo_id)

        .order_by(Booking.booking_time.desc())

        .all()

    )


# ==========================================
# MARK AS PICKED UP
# ==========================================

def mark_as_picked_up(booking_id, ngo_id):

    booking = Booking.query.filter_by(

        id=booking_id,

        ngo_id=ngo_id

    ).first()

    if booking is None:
        return False

    booking.booking_status = "Picked Up"

    booking.food.status = "Picked Up"

    booking.pickup_time = datetime.now()

    db.session.commit()

    # Notify Donor
    create_notification(

        receiver_type="Donor",

        receiver_id=booking.food.donor_id,

        title="Food Picked Up",

        message=f"The NGO has collected '{booking.food.food_name}'."

    )

    return True