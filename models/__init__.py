from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .donation import FoodDonation
from .booking import Booking
from .kyc import KYC