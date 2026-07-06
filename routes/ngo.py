from flask import (
    Blueprint,
    session,
    redirect,
    url_for,
    render_template,
    flash
)

from controllers.ngo_controller import (
    get_dashboard_data,
    get_available_food,
    get_food_by_id,
    book_food,
    get_my_bookings,
    mark_as_picked_up
)
ngo = Blueprint(
    "ngo",
    __name__,
    url_prefix="/ngo"
)

# ==========================================
# NGO DASHBOARD
# ==========================================

@ngo.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )

    data = get_dashboard_data(
        session["user_id"]
    )

    return render_template(
        "ngo/dashboard.html",
        **data
    )


# ==========================================
# AVAILABLE FOOD
# ==========================================

@ngo.route("/available-food")
def available_food():

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )

    food = get_available_food()

    return render_template(
        "ngo/available_food.html",
        food=food
    )


# ==========================================
# FOOD DETAILS
# ==========================================

@ngo.route("/food/<int:food_id>")
def food_details(food_id):

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )

    donation = get_food_by_id(food_id)

    if donation is None:

        flash(
            "Food donation not found.",
            "danger"
        )

        return redirect(
            url_for("ngo.available_food")
        )

    return render_template(
        "ngo/food_details.html",
        donation=donation
    )
    
# ==========================================
# BOOK FOOD
# ==========================================

@ngo.route("/book-food/<int:food_id>", methods=["POST"])
def book_food_route(food_id):

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )

    donation = get_food_by_id(food_id)

    if donation is None:

        flash(
            "Food donation not found.",
            "danger"
        )

        return redirect(
            url_for("ngo.available_food")
        )

    book_food(
        food_id,
        session["user_id"]
    )

    flash(
        "Food booked successfully!",
        "success"
    )

    return redirect(
        url_for("ngo.my_bookings")
    )
# ==========================================
# MY BOOKINGS
# ==========================================

@ngo.route("/my-bookings")
def my_bookings():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    bookings = get_my_bookings(
        session["user_id"]
    )

    return render_template(
        "ngo/my_bookings.html",
        bookings=bookings
    )
# ==========================================
# MARK AS PICKED UP
# ==========================================

@ngo.route("/pickup/<int:booking_id>", methods=["POST"])
def pickup_food(booking_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    success = mark_as_picked_up(
        booking_id,
        session["user_id"]
    )

    if success:

        flash(
            "Food marked as picked up successfully!",
            "success"
        )

    else:

        flash(
            "Unable to update pickup status.",
            "danger"
        )

    return redirect(
        url_for("ngo.my_bookings")
    )