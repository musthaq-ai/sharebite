
from datetime import datetime
from flask import session

import math
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
# DISTANCE CALCULATION (HAVERSINE)
# ==========================================

def calculate_distance(lat1, lon1, lat2, lon2):

    R = 6371  # Earth radius in KM

    lat1 = math.radians(float(lat1))
    lon1 = math.radians(float(lon1))
    lat2 = math.radians(float(lat2))
    lon2 = math.radians(float(lon2))

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return R * c
# ==========================================
# AVAILABLE FOOD
# ==========================================
# ==========================================
# AVAILABLE FOOD (Nearby First)
# ==========================================
# ==========================================
# AVAILABLE FOOD (Smart Radius Search)
# ==========================================

def get_available_food():

    ngo_lat = session.get("current_latitude")
    ngo_lng = session.get("current_longitude")

    foods = FoodDonation.query.filter_by(
        status="Available"
    ).all()

    if not ngo_lat or not ngo_lng:

        return foods

    # Search radius levels (KM)
    radius_levels = [5, 10, 20]

    for radius in radius_levels:

        nearby_food = []

        for food in foods:

            if food.latitude is None or food.longitude is None:

                continue

            distance = calculate_distance(

                ngo_lat,

                ngo_lng,

                food.latitude,

                food.longitude

            )

            food.distance = round(distance, 2)

            if distance <= radius:

                nearby_food.append(food)

        if nearby_food:

            nearby_food.sort(

                key=lambda x: x.distance

            )

            print(f"Nearby food found within {radius} KM")

            return nearby_food

    # -----------------------------------
    # No food inside 20 KM
    # Return all foods sorted by distance
    # -----------------------------------

    for food in foods:

        if food.latitude is None or food.longitude is None:

            continue

        food.distance = round(

            calculate_distance(

                ngo_lat,

                ngo_lng,

                food.latitude,

                food.longitude

            ),

            2

        )

    foods.sort(

        key=lambda x: x.distance

    )

    print("No nearby food. Showing all.")

    return foods

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