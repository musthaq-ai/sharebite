import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Google Maps
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
    
    # Brevo SMTP
    # ==========================================
# Brevo SMTP
# ==========================================

    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

# SMTP Login (Brevo)
    SMTP_LOGIN = os.getenv("SMTP_LOGIN")

# SMTP Password (SMTP Key)
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# Verified Sender Email
    SMTP_SENDER = os.getenv("SMTP_SENDER")

    SMTP_SENDER_NAME = os.getenv("SMTP_SENDER_NAME", "ShareBite")
    # Database
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD", ""))
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://"
        f"{DB_USER}:{DB_PASSWORD}@"
        f"{DB_HOST}:{DB_PORT}/"
        f"{DB_NAME}?sslmode=require"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Uploads
    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "static",
        "uploads"
    )

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024