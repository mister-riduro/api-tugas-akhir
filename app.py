from flask import Flask
from controllers.auth.register import register
from controllers.auth.login import login
from controllers.nearest_event.nearest_event import nearestEvent
from controllers.provinces.provinces import provinces
from controllers.tourism_facilities.tourism_facilities import tourismFacilities
from controllers.tourisms.tourisms import tourisms
from controllers.tourism_type.tourism_type import tourism_type
from controllers.hotel_facilities.hotel_facilities import hotelFacilities
from controllers.hotels.hotels import hotels
from controllers.favorite.favorite import favorite
from flask_jwt_extended import JWTManager
from helpers import initializeENV

import os

app = Flask(__name__)

initializeENV()
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

app.register_blueprint(register)
app.register_blueprint(login)
app.register_blueprint(nearestEvent)
app.register_blueprint(provinces)
app.register_blueprint(tourismFacilities)
app.register_blueprint(tourisms)
app.register_blueprint(tourism_type)
app.register_blueprint(hotelFacilities)
app.register_blueprint(hotels)
app.register_blueprint(favorite)
JWTManager(app)

if __name__ == "__app__":
    app.run()