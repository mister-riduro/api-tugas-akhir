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
    provinceName = request.form.get('province_name')
    propertyType = request.form.get('type')
    hotelCity = request.form.get('city')
    hotelAddress = request.form.get('address')
    hotelRating = request.form.get('rating')
    minPrice = request.form.get('min_price')
    maxPrice = request.form.get('max_price')
    cluster = request.form.get('cluster')
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

    cur.execute("""
                INSERT INTO hotels (
                    hotel_image,
                    hotel_name,
                    property_type,
                    hotel_city,
                    province_name,
                    hotel_address,
                    hotel_rating,
                    min_price,
                    max_price,
                    latitude,
                    longitude,
                    cluster,
                    created_at,
                    updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING hotel_id;""",
                    (hotelImageURL,
                    hotelName, 
                    propertyType, 
                    hotelCity,
                    provinceName, 
                    hotelAddress,
                    hotelRating,
                    maxPrice,
                    minPrice, 
                    latitude,
                    longitude,
                    cluster,
                    createdAt,
                    updatedAt,)
                )
    conn.commit()
    returningID = cur.fetchone()[0]

    cur.execute("SELECT * FROM hotels WHERE hotel_id = %s", (returningID,))
    result = cur.fetchone()

    data = insertOneData(result, [])

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
        result = insertMultipleData(hotel, cur)
    
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
    
    cur.execute("SELECT hfacilities.hfacilities_id, hfacilities.facilities_name, hfacilities.facilities_image FROM tourisms JOIN hfacilities ON hfacilities.hotel_id = %s", (hotel_id,))
    fetchedFacilties = cur.fetchall()

    facilities = []

    if len(fetchedFacilties) == 0:
        facilities = []
    else:
        for facil in fetchedFacilties:
            facilities.append({
                "id" : facil[0],
                "name" : facil[1],
                "image" : facil[2]
            })

    data = insertOneData(result, facilities)
    
    return responseSuccessJSON(200, "success get hotel", data)


@hotels.route("/v1/hotel/<hotel_id>", methods = ['PUT'])
@jwt_required()
def updateHotel(hotel_id):
    hotelImage = request.files['image']
    hotelName = request.form.get('name')
    provinceName = request.form.get('province_name')
    propertyType = request.form.get('type')
    hotelCity = request.form.get('city')
    hotelAddress = request.form.get('address')
    hotelRating = request.form.get('rating')
    minPrice = request.form.get('min_price')
    maxPrice = request.form.get('max_price')
    cluster = request.form.get('cluster')
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
    
    cur.execute("""
                UPDATE hotels SET
                    hotel_image = %s,
                    hotel_name = %s,
                    property_type = %s,
                    hotel_city = %s,
                    province_name = %s,
                    hotel_address = %s,
                    hotel_rating = %s,
                    min_price = %s,
                    max_price = %s,
                    lattitude = %s,
                    longitude = %s,
                    cluster = %s,
                    updated_at = %s;""",
                    (hotelImageURL,
                    hotelName, 
                    propertyType, 
                    hotelCity,
                    provinceName, 
                    hotelAddress,
                    hotelRating,
                    minPrice,
                    maxPrice, 
                    latitude,
                    longitude,
                    cluster,
                    updatedAt,)
                )
    conn.commit()

    cur.execute("SELECT * FROM hotels WHERE hotel_id = %s", (hotel_id))
    updatedResult = cur.fetchone()

    cur.execute("SELECT hfacilities.hfacilities_id, hfacilities.facilities_name, hfacilities.facilities_image FROM tourisms JOIN hfacilities ON hfacilities.hotel_id = %s", (hotel_id,))
    fetchedFacilties = cur.fetchall()

    facilities = []

    if len(fetchedFacilties) == 0:
        facilities = []
    else:
        for item in fetchedFacilties:
            facilities.append({
                "id" : item[0],
                "name" : item[1],
                "image" : item[2]
            })

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

def insertOneData(item, facilities):
    if facilities == []:
        facilities = []

    data = {
        "id" : item[0],
        "image" : item[1],
        "name" : item[2],
        "property_type" : item[3],
        "city" : item[4],
        "province_name" : item[5],
        "address" : item[6],
        "rating" : item[7],
        "min_price" : item[8],
        "max_price" : item[9],
        "facilities" : facilities,
        "latitude" : item[10],
        "longitude" : item[11],
        "cluster" : item[12],
        "created_at" : item[13],
        "updated_at" : item[14]
    }

    return data

def insertMultipleData(items, cur):
    datas = []

    for item in items:
        cur.execute("SELECT hfacilities.hfacilities_id, hfacilities.facilities_name FROM tourisms JOIN hfacilities ON hfacilities.hotel_id = %s", (item[0],))
        fetchedFacilties = cur.fetchall()

        facilities = []

        if len(fetchedFacilties) == 0:
            facilities = []
        else:
            for facil in fetchedFacilties:
                facilities.append({
                    "id" : facil[0],
                    "name" : facil[2],
                    "image" : facil[3]
                })


        datas.append({
            "id" : item[0],
            "image" : item[1],
            "name" : item[2],
            "property_type" : item[3],
            "city" : item[4],
            "province_name" : item[5],
            "address" : item[6],
            "rating" : item[7],
            "min_price" : item[8],
            "max_price" : item[9],
            "facilities" : facilities,
            "latitude" : item[10],
            "longitude" : item[11],
            "cluster" : item[12],
            "created_at" : item[13],
            "updated_at" : item[14]
        })
    
    return datas