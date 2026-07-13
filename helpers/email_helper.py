import random
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import current_app


# ==========================================
# GENERATE 6-DIGIT OTP
# ==========================================

def generate_otp():

    return str(random.randint(100000, 999999))


# ==========================================
# SEND OTP EMAIL
# ==========================================

def send_otp_email(receiver_email, otp):

    smtp_server = current_app.config["SMTP_SERVER"]
    smtp_port = current_app.config["SMTP_PORT"]

    # SMTP Login Credentials
    smtp_login = current_app.config["SMTP_LOGIN"]
    smtp_password = current_app.config["SMTP_PASSWORD"]

    # Verified Sender
    sender_email = current_app.config["SMTP_SENDER"]
    sender_name = current_app.config["SMTP_SENDER_NAME"]

    print("\n========== SMTP CONFIG ==========")
    print("SERVER :", smtp_server)
    print("PORT   :", smtp_port)
    print("LOGIN  :", smtp_login)
    print("SENDER :", sender_email)
    print("=================================\n")

    message = MIMEMultipart("alternative")

    message["Subject"] = "ShareBite Email Verification OTP"
    message["From"] = f"{sender_name} <{sender_email}>"
    message["To"] = receiver_email

    html = f"""
    <html>
    <body style="font-family:Arial;background:#f4f6f9;padding:30px;">
        <div style="
            max-width:600px;
            margin:auto;
            background:white;
            border-radius:10px;
            padding:40px;
            box-shadow:0 0 15px rgba(0,0,0,.08);
        ">

            <h2 style="color:#198754;text-align:center;">
                ShareBite
            </h2>

            <h3>Verify Your Email</h3>

            <p>
                Thank you for registering with ShareBite.
            </p>

            <p>
                Please use the following One-Time Password (OTP):
            </p>

            <div style="
                font-size:34px;
                font-weight:bold;
                letter-spacing:8px;
                color:#198754;
                text-align:center;
                margin:30px 0;
            ">
                {otp}
            </div>

            <p>
                This OTP is valid for <strong>5 minutes</strong>.
            </p>

            <hr>

            <p style="font-size:12px;color:gray;">
                If you did not request this registration,
                you may safely ignore this email.
            </p>

        </div>
    </body>
    </html>
    """

    message.attach(MIMEText(html, "html"))

    try:

        print("Connecting to SMTP...")

        server = smtplib.SMTP(
            smtp_server,
            smtp_port
        )

        print("Connected")

        server.starttls()

        print("TLS Started")

        # Login using Brevo SMTP Login
        server.login(
            smtp_login,
            smtp_password
        )

        print("Login Successful")

        # Send from your verified sender email
        server.sendmail(
            sender_email,
            receiver_email,
            message.as_string()
        )

        print("Email Sent Successfully")

        server.quit()

        return True

    except Exception as e:

        print("SMTP ERROR:", e)

        return False