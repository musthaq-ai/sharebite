from flask import (
    Blueprint,
    session,
    redirect,
    url_for,
    render_template,
    request
)

from controllers.admin_controller import (
    get_dashboard_data,
    get_all_users,
    delete_user,
    get_all_donations,
    admin_delete_donation,
    get_all_bookings,
    get_kyc_requests,
    approve_kyc,
    reject_kyc,
    get_user_details
)
admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


# ==========================================
# ADMIN DASHBOARD
# ==========================================

@admin.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "Admin":
        return redirect(url_for("auth.login"))

    data = get_dashboard_data()

    return render_template(
        "admin/dashboard.html",
        **data
    )


# ==========================================
# MANAGE USERS
# ==========================================

@admin.route("/users")
def users():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "Admin":
        return redirect(url_for("auth.login"))

    search = request.args.get("search")

    role = request.args.get("role")

    users = get_all_users(
        search,
        role
    )

    return render_template(
        "admin/users.html",
        users=users
    )
# ==========================================
# VIEW USER DETAILS
# ==========================================

@admin.route("/user/<int:user_id>")
def user_details(user_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "Admin":
        return redirect(url_for("auth.login"))

    user = get_user_details(user_id)

    if user is None:
        return redirect(url_for("admin.users"))

    return render_template(
        "admin/user_details.html",
        user=user
    )

# ==========================================
# DELETE USER
# ==========================================

@admin.route("/user/delete/<int:user_id>", methods=["POST"])
def delete_user_route(user_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "Admin":
        return redirect(url_for("auth.login"))

    delete_user(user_id)

    return redirect(
        url_for("admin.users")
    )
    
# ==========================================
# MANAGE DONATIONS
# ==========================================

@admin.route("/donations")
def donations():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "Admin":
        return redirect(url_for("auth.login"))

    search = request.args.get("search")

    status = request.args.get("status")

    donations = get_all_donations(
        search,
        status
    )

    return render_template(
        "admin/donations.html",
        donations=donations
    )


# ==========================================
# DELETE DONATION
# ==========================================

@admin.route("/donation/delete/<int:donation_id>", methods=["POST"])
def delete_donation_route(donation_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "Admin":
        return redirect(url_for("auth.login"))

    admin_delete_donation(
        donation_id
    )

    return redirect(
        url_for("admin.donations")
    )
    
# ==========================================
# MANAGE BOOKINGS
# ==========================================

@admin.route("/bookings")
def bookings():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "Admin":
        return redirect(url_for("auth.login"))

    status = request.args.get("status")

    bookings = get_all_bookings(status)

    return render_template(
        "admin/bookings.html",
        bookings=bookings
    )
# ==========================================
# KYC REQUESTS
# ==========================================

@admin.route("/kyc")
def kyc_requests():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "Admin":
        return redirect(url_for("auth.login"))

    requests = get_kyc_requests()

    return render_template(
        "admin/kyc_requests.html",
        requests=requests
    )


# ==========================================
# APPROVE KYC
# ==========================================

@admin.route("/kyc/approve/<int:kyc_id>", methods=["POST"])
def approve_kyc_route(kyc_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "Admin":
        return redirect(url_for("auth.login"))

    approve_kyc(kyc_id)

    return redirect(
        url_for("admin.kyc_requests")
    )


# ==========================================
# REJECT KYC
# ==========================================

@admin.route("/kyc/reject/<int:kyc_id>", methods=["POST"])
def reject_kyc_route(kyc_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "Admin":
        return redirect(url_for("auth.login"))

    reason = request.form.get("reason")

    reject_kyc(
        kyc_id,
        reason
    )

    return redirect(
        url_for("admin.kyc_requests")
    )