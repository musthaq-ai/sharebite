from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    request
)

from controllers.notification_controller import (
    get_notifications,
    mark_as_read
)

notification = Blueprint(
    "notification",
    __name__,
    url_prefix="/notifications"
)


# ==========================================
# NOTIFICATIONS
# ==========================================

@notification.route("/")
def index():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    role = session["role"]

    notifications = get_notifications(

        role,

        session["user_id"]

    )

    return render_template(

        "notification/index.html",

        notifications=notifications

    )
    
# ==========================================
# MARK AS READ
# ==========================================

@notification.route("/read/<int:notification_id>", methods=["POST"])
def read(notification_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    mark_as_read(

        notification_id,

        session["role"],

        session["user_id"]

    )

    return redirect(
        url_for("notification.index")
    )