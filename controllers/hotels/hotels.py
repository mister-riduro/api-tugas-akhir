from flask import Blueprint, request
from flask_cors import CORS
from flask_jwt_extended import jwt_required

from helpers import *

from datetime import datetime

hotels = Blueprint('hotels', __name__)
cors = CORS(hotels, resources={r"/v1/*": {"origins": "*"}})

@hotels.route("/v1/hotel", methods = ['POST'])
@jwt_required()
def createHotel():
    hotelImage = request.files['image']
    hotelName = request.form.get('name')
    provinceID = request.form.get('province_id')
    propertyType = request.form.get('type')
    hotelCity = request.form.get('city')
    hotelAddress = request.form.get('address')
    hotelRating = request.form.get('rating')
    minPrice = request.form.get('min_price')
    maxPrice = request.form.get('max_price')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    createdAt = datetime.now()
    updatedAt = datetime.now()

    conn = initializeDB()
    cur = conn.cursor()

    if request.files['image'].filename == '':
        hotelImageURL = ""
    else:
        hotelImageURL = uploadImage(hotelImage)
    
    hotelRating = float(hotelRating)
    latitude = float(latitude)
    longitude = float(longitude)
    minPrice = int(minPrice)
    maxPrice = int(maxPrice)

    cur.execute("SELECT * FROM provinces WHERE province_id = %s;", (provinceID,))
    province = cur.fetchone()

    if province is None:
        return responseFailJSON(404, "province not found")
    
    provinceName = province[2]

    cur.execute("""
                INSERT INTO hotels (
                    hotel_image,
                    hotel_name,
                    property_type,
                    hotel_city,
                    province_id,
                    province_name,
                    hotel_address,
                    hotel_rating,
                    min_price,
                    max_price,
                    lattitude,
                    longitude,
                    created_at,
                    updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING hotel_id;""",
                    (hotelImageURL,
                    hotelName, 
                    propertyType, 
                    hotelCity,
                    provinceID, 
                    provinceName,
                    hotelAddress,
                    hotelRating,
                    maxPrice,
                    minPrice, 
                    latitude,
                    longitude,
                    createdAt,
                    updatedAt,)
                )
    conn.commit()
    returningID = cur.fetchone()[0]

    cur.execute("SELECT * FROM hotels WHERE hotel_id = %s", (returningID,))
    result = cur.fetchone()

    data = insertOneData(result)

    return responseSuccessJSON(201, "success create hotel", data)


@hotels.route("/v1/hotel", methods = ['GET'])
@jwt_required()
def getAllHotel():
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM hotels")
    hotel = cur.fetchall()

    result = []

    if len(hotel) != 0:
        result = insertMultipleData(hotel)
    
    return responseSuccessJSON(200, "success get all hotel", result)

@hotels.route("/v1/hotel/<hotel_id>", methods = ['GET'])
@jwt_required()
def getOneHotel(hotel_id):
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM hotels WHERE hotel_id = %s", (hotel_id))
    result = cur.fetchone()

    if result is None:
        return responseFailJSON(404, "hotel not found")
    
    return responseSuccessJSON(200, "success get hotel", result)


@hotels.route("/v1/hotel/<hotel_id>", methods = ['PUT'])
@jwt_required()
def updateHotel(hotel_id):
    hotelImage = request.files['image']
    hotelName = request.form.get('name')
    provinceID = request.form.get('province_id')
    propertyType = request.form.get('type')
    hotelCity = request.form.get('city')
    hotelAddress = request.form.get('address')
    hotelRating = request.form.get('rating')
    minPrice = request.form.get('min_price')
    maxPrice = request.form.get('max_price')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    updatedAt = datetime.now()

    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM hotels WHERE hotel_id = %s", (hotel_id))
    result = cur.fetchone()

    if result is None:
        return responseFailJSON(404, "hotel not found")
    
    if request.files['image'].filename == '' and result[1] == "":
        hotelImageURL = ""
    elif request.files['image'].filename == '' and result[1] != "":
        hotelImageURL = result[1]
    else:
        hotelImageURL = uploadImage(hotelImage)

    cur.execute("SELECT * FROM provinces WHERE province_id = %s;", (provinceID,))
    province = cur.fetchone()

    if province is None:
        return responseFailJSON(404, "province not found")
    
    provinceName = province[2]
    
    cur.execute("""
                UPDATE hotels SET
                    hotel_image = %s,
                    hotel_name = %s,
                    property_type = %s,
                    hotel_city = %s,
                    province_id = %s,
                    province_name = %s,
                    hotel_address = %s,
                    hotel_rating = %s,
                    min_price = %s,
                    max_price = %s,
                    lattitude = %s,
                    longitude = %s,
                    updated_at = %s;""",
                    (hotelImageURL,
                    hotelName, 
                    propertyType, 
                    hotelCity,
                    provinceID, 
                    provinceName,
                    hotelAddress,
                    hotelRating,
                    maxPrice,
                    minPrice, 
                    latitude,
                    longitude,
                    updatedAt,)
                )
    conn.commit()

    cur.execute("SELECT * FROM hotels WHERE hotel_id = %s", (hotel_id))
    updatedResult = cur.fetchone()

    data = insertOneData(updatedResult)

    return responseSuccessJSON(200, "success update hotel", data)

@hotels.route("/v1/hotel/<hotel_id>", methods = ['DELETE'])
@jwt_required()
def deleteHotel(hotel_id):
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM hotels WHERE hotel_id = %s", (hotel_id))
    result = cur.fetchone()

    if result is None:
        return responseFailJSON(404, "hotel not found")

    cur.execute("DELETE FROM hotels WHERE hotel_id = %s", (hotel_id))
    conn.commit()
    
    return responseSuccessJSON(200, "success delete hotel", "")

def insertOneData(item):
    data = {
        "id" : item[0],
        "image" : item[1],
        "name" : item[2],
        "property_type" : item[3],
        "city" : item[4],
        "province_id" : item[5],
        "province_name" : item[6],
        "address" : item[7],
        "rating" : item[8],
        "min_price" : item[9],
        "max_price" : item[10],
        "latitude" : item[11],
        "longitude" : item[12],
        "created_at" : item[13],
        "updated_at" : item[14]
    }

    return data

def insertMultipleData(items):
    datas = []

    for item in items:
        datas.append({
            "id" : item[0],
            "image" : item[1],
            "name" : item[2],
            "property_type" : item[3],
            "city" : item[4],
            "province_id" : item[5],
            "province_name" : item[6],
            "address" : item[7],
            "rating" : item[8],
            "min_price" : item[9],
            "max_price" : item[10],
            "latitude" : item[11],
            "longitude" : item[12],
            "created_at" : item[13],
            "updated_at" : item[14]
        })
    
    return datas