from flask import jsonify
from controllers.donor_controller import verify_qr
from controllers.donor_controller import verify_booking_qr

from flask import (
    Blueprint,
    session,
    redirect,
    url_for,
    render_template,
    request,
    flash
)

from controllers.donor_controller import (
    get_dashboard_data,
    get_my_donations,
    save_food,
    get_donation_by_id,
    update_donation,
    delete_donation,
    get_booking_requests,
    accept_booking,
    reject_booking,
    complete_donation
)

donor = Blueprint(
    "donor",
    __name__,
    url_prefix="/donor"
)


# =====================================================
# DASHBOARD
# =====================================================

@donor.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    data = get_dashboard_data(session["user_id"])

    return render_template(
        "donor/dashboard.html",
        **data
    )


# =====================================================
# ADD FOOD
# =====================================================

@donor.route("/add-food", methods=["GET", "POST"])
def add_food():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        save_food(
            request.form,
            request.files,
            session["user_id"]
        )

        flash(
            "Food donation added successfully!",
            "success"
        )

        return redirect(
            url_for("donor.my_donations")
        )

    return render_template(
        "donor/add_food.html",
        donation=None
    )


# =====================================================
# MY DONATIONS
# =====================================================

@donor.route("/my-donations")
def my_donations():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    search = request.args.get("search", "")

    status = request.args.get("status", "All")

    donations = get_my_donations(
        session["user_id"],
        search,
        status
    )

    return render_template(
        "donor/my_donations.html",
        donations=donations,
        search=search,
        status=status
    )
# =====================================================
# VIEW DONATION
# =====================================================

@donor.route("/view-donation/<int:donation_id>")
def view_donation(donation_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    donation = get_donation_by_id(
        donation_id,
        session["user_id"]
    )

    if donation is None:

        flash(
            "Donation not found.",
            "danger"
        )

        return redirect(
            url_for("donor.my_donations")
        )

    return render_template(
        "donor/view_donation.html",
        donation=donation
    )
# =====================================================
# EDIT DONATION
# =====================================================

@donor.route("/edit-donation/<int:donation_id>", methods=["GET", "POST"])
def edit_donation(donation_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    donation = get_donation_by_id(
        donation_id,
        session["user_id"]
    )

    if donation is None:

        flash(
            "Donation not found.",
            "danger"
        )

        return redirect(
            url_for("donor.my_donations")
        )

    if request.method == "POST":

        update_donation(
            donation,
            request.form,
            request.files
        )

        flash(
            "Donation updated successfully!",
            "success"
        )

        return redirect(
            url_for("donor.my_donations")
        )

    return render_template(
        "donor/edit_food.html",
        donation=donation
    )


# =====================================================
# DELETE DONATION
# =====================================================

@donor.route("/delete-donation/<int:donation_id>", methods=["POST"])
def delete_food(donation_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    donation = get_donation_by_id(
        donation_id,
        session["user_id"]
    )

    if donation is None:

        flash(
            "Donation not found.",
            "danger"
        )

        return redirect(
            url_for("donor.my_donations")
        )

    delete_donation(donation)

    flash(
        "Donation deleted successfully!",
        "success"
    )

    return redirect(
        url_for("donor.my_donations")
    )
# =====================================================
# BOOKING REQUESTS
# =====================================================

@donor.route("/booking-requests")
def booking_requests():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    requests = get_booking_requests(
        session["user_id"]
    )

    return render_template(
        "donor/booking_requests.html",
        requests=requests
    )
# =====================================================
# ACCEPT BOOKING
# =====================================================

@donor.route("/accept-booking/<int:booking_id>", methods=["POST"])
def accept_booking_route(booking_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    success = accept_booking(
        booking_id,
        session["user_id"]
    )

    if success:

        flash(
            "Booking accepted successfully!",
            "success"
        )

    else:

        flash(
            "Unable to accept booking.",
            "danger"
        )

    return redirect(
        url_for("donor.booking_requests")
    )
# =====================================================
# REJECT BOOKING
# =====================================================

@donor.route("/reject-booking/<int:booking_id>", methods=["POST"])
def reject_booking_route(booking_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    success = reject_booking(
        booking_id,
        session["user_id"]
    )

    if success:

        flash(
            "Booking rejected successfully!",
            "success"
        )

    else:

        flash(
            "Unable to reject booking.",
            "danger"
        )

    return redirect(
        url_for("donor.booking_requests")
    )
    
# =====================================================
# COMPLETE DONATION
# =====================================================

@donor.route("/complete-donation/<int:booking_id>", methods=["POST"])
def complete_donation_route(booking_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    success = complete_donation(
        booking_id,
        session["user_id"]
    )

    if success:

        flash(
            "Donation marked as completed!",
            "success"
        )

    else:

        flash(
            "Unable to complete donation.",
            "danger"
        )

    return redirect(
        url_for("donor.booking_requests")
    )
    
# =====================================================
# SCAN NGO QR
# =====================================================

@donor.route("/scan-qr")
def scan_qr():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return render_template(
        "donor/scan_qr.html"
    )


# =====================================================
# VERIFY QR
# =====================================================

@donor.route("/verify-ngo", methods=["POST"])
def verify_ngo():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Please login."
        }), 401

    data = request.get_json()

    qr_data = data.get("qr")

    return verify_booking_qr(qr_data) 
# =====================================================
# LOGOUT
# =====================================================

@donor.route("/logout")
def logout():

    session.clear()

    flash(
        "Logged out successfully.",
        "success"
    )

    return redirect(
        url_for("auth.login")
    )