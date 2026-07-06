from functools import wraps

from flask import session, redirect, url_for


# ==========================================
# LOGIN REQUIRED
# ==========================================

def login_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        if "user_id" not in session:

            return redirect(
                url_for("auth.login")
            )

        return f(*args, **kwargs)

    return decorated


# ==========================================
# ROLE REQUIRED
# ==========================================

def role_required(role):

    def decorator(f):

        @wraps(f)
        def decorated(*args, **kwargs):

            if "user_id" not in session:

                return redirect(
                    url_for("auth.login")
                )

            if session.get("role") != role:

                return redirect(
                    url_for("auth.login")
                )

            return f(*args, **kwargs)

        return decorated

    return decorator