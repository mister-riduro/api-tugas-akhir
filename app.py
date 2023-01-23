from flask import Flask, json, request
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
from controllers.recommendation.recommendation import recommendation
from controllers.users.users import users
from flask_jwt_extended import JWTManager, jwt_required, get_jwt
from helpers import *
from datetime import timedelta

import os
import redis

app = Flask(__name__)

initializeENV()
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.secret_key = os.getenv('APP_SECRET_KEY')

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
app.register_blueprint(recommendation)
app.register_blueprint(users)
jwt = JWTManager(app)

jwt_redis_blocklist = redis.Redis(
    host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), password=os.getenv('REDIS_PASS')
)

ACCESS_EXPIRES = timedelta(hours=1)

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)

    return token_in_redis is not None

@app.route("/v1/logout", methods = ['DELETE'])
@jwt_required()
def logoutUser():
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)

    return_json = {
        'message' : "Access token revoked"
    }

    return return_json

if __name__ == "__main__":
    app.run()