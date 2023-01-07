from flask import Blueprint, request
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity

from helpers import *

from datetime import datetime

favorite = Blueprint('favorite', __name__)
cors = CORS(favorite, resources={r"/v1/*": {"origins": "*"}})

@favorite.route("/v1/favorite/h/a/<hotel_id>", methods = ['POST'])
@jwt_required()
def addHotelFavorite(hotel_id):
    conn = initializeDB()
    cur = conn.cursor()

    userID = get_jwt_identity()

    createdAt = datetime.now()
    updatedAt = datetime.now()

    cur.execute("SELECT * FROM hotels WHERE hotel_id = %s", (hotel_id,))
    result = cur.fetchone()

    if result is None:
        return responseFailJSON(404, "hotel not found")
    
    cur.execute("INSERT INTO favorite_hotel(user_id, hotel_id, created_at, updated_at) VALUES(%s, %s, %s, %s);", (userID, hotel_id, createdAt, updatedAt))
    conn.commit()

    return responseSuccessJSON(201, "success add hotel to favorite", "")

@favorite.route("/v1/favorite/h/r/<hotel_id>", methods = ['DELETE'])
@jwt_required()
def removeHotelFavorite(hotel_id):
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM hotels WHERE hotel_id = %s", (hotel_id,))
    result = cur.fetchone()

    if result is None:
        return responseFailJSON(404, "hotel not found")
    
    cur.execute("SELECT * FROM favorite_hotel WHERE hotel_id = %s", (hotel_id,))
    result = cur.fetchone()

    if result is None:
        return responseFailJSON(404, "hotel is not in favorite")
    
    cur.execute("DELETE FROM favorite_hotel WHERE hotel_id = %s;", (hotel_id))
    conn.commit()

    return responseSuccessJSON(200, "success delete hotel from favorite", "")

@favorite.route("/v1/favorite/t/a/<tourism_id>", methods = ['POST'])
@jwt_required()
def addTourismFavorite(tourism_id):
    conn = initializeDB()
    cur = conn.cursor()

    userID = get_jwt_identity()

    createdAt = datetime.now()
    updatedAt = datetime.now()

    cur.execute("SELECT * FROM tourisms WHERE tourism_id = %s", (tourism_id,))
    result = cur.fetchone()

    if result is None:
        return responseFailJSON(404, "tourism not found")
    
    cur.execute("INSERT INTO favorite_tourism(user_id, tourism_id, created_at, updated_at) VALUES(%s, %s, %s, %s);", (userID, tourism_id, createdAt, updatedAt))
    conn.commit()

    return responseSuccessJSON(201, "success add tourism to favorite", "")

@favorite.route("/v1/favorite/t/r/<tourism_id>", methods = ['DELETE'])
@jwt_required()
def removeTourismFavorite(tourism_id):
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tourisms WHERE tourism_id = %s", (tourism_id,))
    result = cur.fetchone()

    if result is None:
        return responseFailJSON(404, "tourism not found")
    
    cur.execute("SELECT * FROM favorite_tourism WHERE tourism_id = %s", (tourism_id,))
    result = cur.fetchone()

    if result is None:
        return responseFailJSON(404, "tourism is not in favorite")
    
    cur.execute("DELETE FROM favorite_tourism WHERE tourism_id = %s;", (tourism_id))
    conn.commit()

    return responseSuccessJSON(200, "success delete tourism from favorite", "")