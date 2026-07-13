from flask import Flask
from config import Config
from models import db
from routes.ngo import ngo
from flask import session
from routes.location import location

from models.temp_registration import TempRegistration
from routes.admin import admin
from controllers.notification_controller import get_unread_count
# Import Models
from models.donation import FoodDonation
from models.booking import Booking
from models.user import User
from routes.kyc import kyc

from routes.home import home
from flask import current_app

# Import Blueprints
from routes.auth import auth
from routes.donor import donor

from routes.notification import notification
app = Flask(__name__)

# Load configuration
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Register Blueprints
app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(donor)
app.register_blueprint(ngo)
app.register_blueprint(notification)
app.register_blueprint(admin)
app.register_blueprint(kyc)
app.register_blueprint(location)
@app.context_processor
def inject_globals():

    if "user_id" in session and "role" in session:

        unread_count = get_unread_count(

            session["role"],

            session["user_id"]

        )

    else:

        unread_count = 0

    return {

        "unread_notifications": unread_count,

        "config": {

            "GOOGLE_MAPS_API_KEY":
            current_app.config["GOOGLE_MAPS_API_KEY"]

        }

    }
    

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)