import os
import qrcode

from flask import current_app


def generate_booking_qr(booking):

    folder = os.path.join(
        current_app.static_folder,
        "qr_codes"
    )

    os.makedirs(folder, exist_ok=True)

    filename = f"booking_{booking.id}.png"

    filepath = os.path.join(folder, filename)

    # Data inside QR
    qr_data = f"{booking.id}|{booking.qr_token}"

    img = qrcode.make(qr_data)

    img.save(filepath)

    return filename