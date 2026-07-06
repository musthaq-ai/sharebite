from datetime import datetime

from models import db
from models.notification import Notification


# ==========================================
# CREATE NOTIFICATION
# ==========================================

def create_notification(

    receiver_type,

    receiver_id,

    title,

    message

):

    notification = Notification(

        receiver_type=receiver_type,

        receiver_id=receiver_id,

        title=title,

        message=message,

        created_at=datetime.now()

    )

    db.session.add(notification)

    db.session.commit()


# ==========================================
# GET NOTIFICATIONS
# ==========================================

def get_notifications(

    receiver_type,

    receiver_id

):

    return (

        Notification.query

        .filter_by(

            receiver_type=receiver_type,

            receiver_id=receiver_id

        )

        .order_by(

            Notification.created_at.desc()

        )

        .all()

    )
    
# ==========================================
# UNREAD COUNT
# ==========================================

def get_unread_count(receiver_type, receiver_id):

    return (

        Notification.query

        .filter_by(

            receiver_type=receiver_type,

            receiver_id=receiver_id,

            status="Unread"

        )

        .count()

    )


# ==========================================
# MARK AS READ
# ==========================================

def mark_as_read(notification_id, receiver_type, receiver_id):

    notification = Notification.query.filter_by(

        id=notification_id,

        receiver_type=receiver_type,

        receiver_id=receiver_id

    ).first()

    if notification:

        notification.status = "Read"

        db.session.commit()