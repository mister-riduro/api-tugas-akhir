from flask import Blueprint, request
from flask_cors import CORS
from flask_jwt_extended import jwt_required

from helpers import *

from datetime import datetime

tourisms = Blueprint('tourisms', __name__)
cors = CORS(tourisms, resources={r"/v1/*": {"origins": "*"}})

@tourisms.route("/v1/tourisms", methods = ['POST'])
@jwt_required()
def createTourism():
    tourismName = request.form.get('name')
    tourismImage = request.files['image']
    tourismAddress = request.form.get('address')
    tourismTypeID = request.form.get('type_id')
    tourismCity = request.form.get('city')
    provinceID = request.form.get('province_id')
    openHour = request.form.get('open_hour')
    closeHour = request.form.get('close_hour')
    tourismDesc = request.form.get('description')
    entryPrice = request.form.get('entry_price')
    travelingTime = request.form.get('traveling_time')
    roadCondition = request.form.get('road_condition')

    tourismRating = request.form.get('rating')
    lattitude = request.form.get('lattitude')
    longitude = request.form.get('longitude')

    createdAt = datetime.now()
    updatedAt = datetime.now()

    # Change from string to decimal
    tourismRating = float(tourismRating)
    lattitude = float(lattitude)
    longitude = float(longitude)
    entryPrice = int(entryPrice)

    conn = initializeDB()
    cur = conn.cursor()

    if request.files['image'].filename == '':
        tourismImageURL = ""
    else:
        tourismImageURL = uploadImage(tourismImage)

    # Tourism Type
    cur.execute("SELECT * FROM tourism_type WHERE tourism_type_id = %s;", (tourismTypeID,))
    tourismType = cur.fetchone()

    if tourismType is None:
        return_json = {
            "status" : 404,
            "message" : "tourism type not found"
        }

        return return_json
    
    tourismTypeName = tourismType[2]
    
    # Province
    cur.execute("SELECT * FROM provinces WHERE province_id = %s;", (provinceID,))
    province = cur.fetchone()

    if province is None:
        return responseFailJSON(404, "province not found")
    
    provinceName = province[2]

    cur.execute("""
                INSERT INTO tourisms (
                    tourism_name,
                    tourism_image,
                    tourism_address,
                    tourism_type_id,
                    tourism_type,
                    tourism_city,
                    province_id,
                    tourism_province,
                    open_hour,
                    close_hour,
                    tourism_description,
                    entry_price,
                    traveling_time,
                    road_condition,
                    tourism_rating,
                    lattitude,
                    longitude,
                    created_at,
                    updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING tourism_id;""",
                    (tourismName,
                    tourismImageURL, 
                    tourismAddress, 
                    tourismTypeID,
                    tourismTypeName, 
                    tourismCity, 
                    provinceID, 
                    provinceName, 
                    openHour,
                    closeHour,
                    tourismDesc,
                    entryPrice,
                    travelingTime,
                    roadCondition,
                    tourismRating,
                    lattitude,
                    longitude,
                    createdAt,
                    updatedAt,)
                )
    conn.commit()
    returningID = cur.fetchone()[0]

    cur.execute("SELECT * FROM tourisms WHERE tourism_id = %s;", (returningID,))
    result = cur.fetchone()

    return_json = {
        "status" : 201,
        "message" : "success create tourism",
        "data" : {
            "id" : result[0],
            "image" : result[1],
            "name" : result[2],
            "address" : result[3],
            "type_id" : result[4],
            "type" : result[5],
            "city" : result[6],
            "province_id" : result[7],
            "province" : result[8],
            "open_hour" : result[9],
            "close_hour" : result[10],
            "description" : result[11],
            "entry_price" : result[12],
            "traveling_time" : result[13],
            "road_condition" : result[14],
            "rating" : result[15],
            "lattitude" : result[16],
            "longitude" : result[17],
            "created_at" : result[18],
            "updated_at" : result[19]
        }
    }

    return return_json

@tourisms.route("/v1/tourisms/<tourism_id>", methods = ['GET'])
@jwt_required()
def getOneTourism(tourism_id):
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tourisms WHERE tourism_id = %s;", (tourism_id,))
    result = cur.fetchone()

    if result is None:
        return_json = {
            "status" : 404,
            "message" : "tourism not found"
        }

        return return_json

    cur.execute("SELECT tfacilities.tfacilities_id, tfacilities.facilities_name FROM tourisms JOIN tfacilities ON tourisms.tourism_id = %s", (tourism_id,))
    fetchedFacilties = cur.fetchall()

    facilities = []

    if len(fetchedFacilties) == 0:
        facilities = []
    else:
        for item in fetchedFacilties:
            facilities.append({
                "id" : item[0],
                "name" : item[1]
            })
    
    return_json = {
            "status" : 200,
            "message" : "success get tourism",
            "data" : {
                "id" : result[0],
                "image" : result[1],
                "name" : result[2],
                "address" : result[3],
                "type_id" : result[4],
                "type" : result[5],
                "city" : result[6],
                "province_id" : result[7],
                "province" : result[8],
                "open_hour" : result[9],
                "close_hour" : result[10],
                "description" : result[11],
                "entry_price" : result[12],
                "facilities" : facilities,
                "traveling_time" : result[13],
                "road_condition" : result[14],
                "rating" : result[15],
                "lattitude" : result[16],
                "longitude" : result[17],
                "created_at" : result[18],
                "updated_at" : result[19]
            }
    }

    return return_json

@tourisms.route("/v1/tourisms", methods = ['GET'])
@jwt_required()
def getAllTourism():
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tourisms;")
    tourism = cur.fetchall()

    result = []

    for item in tourism:
        cur.execute("SELECT tfacilities.tfacilities_id, tfacilities.facilities_name FROM tourisms JOIN tfacilities ON tourisms.tourism_id = %s", (item[0],))
        fetchedFacilties = cur.fetchall()

        facilities = []

        if len(fetchedFacilties) != 0:
            for item in fetchedFacilties:
                facilities.append({
                    "id" : item[0],
                    "name" : item[1]
                })

        result.append({
            "id" : item[0],
            "image" : item[1],
            "name" : item[2],
            "address" : item[3],
            "type_id" : item[4],
            "type" : item[5],
            "city" : item[6],
            "province_id" : item[7],
            "province" : item[8],
            "open_hour" : item[9],
            "close_hour" : item[10],
            "description" : item[11],
            "entry_price" : item[12],
            "facilities" : facilities,
            "traveling_time" : item[13],
            "road_condition" : item[14],
            "rating" : item[15],
            "lattitude" : item[16],
            "longitude" : item[17],
            "created_at" : item[18],
            "updated_at" : item[19]
        })
    
    return_json = {
            "status" : 200,
            "message" : "success get tourism",
            "data" : result
    }

    return return_json

@tourisms.route("/v1/tourisms/<tourism_id>", methods = ['DELETE'])
@jwt_required()
def deleteTourism(tourism_id):
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tourisms WHERE tourism_id = %s;", (tourism_id,))
    result = cur.fetchone()

    if result is None:
        return_json = {
            "status" : 404,
            "message" : "tourism not found"
        }

        return return_json

    cur.execute("DELETE FROM tourisms WHERE tourism_id = %s;", (tourism_id,))
    conn.commit()
    
    return_json = {
            "status" : 200,
            "message" : "success delete tourism",
            "data" : ""
    }

    return return_json

@tourisms.route("/v1/tourisms/<tourism_id>", methods = ['PUT'])
@jwt_required()
def updateTourism(tourism_id):
    tourismName = request.form.get('name')
    tourismImage = request.files['image']
    tourismAddress = request.form.get('address')
    tourismTypeID = request.form.get('type_id')
    tourismCity = request.form.get('city')
    provinceID = request.form.get('province_id')
    openHour = request.form.get('open_hour')
    closeHour = request.form.get('close_hour')
    tourismDesc = request.form.get('description')
    entryPrice = request.form.get('entry_price')
    travelingTime = request.form.get('traveling_time')
    roadCondition = request.form.get('road_condition')

    tourismRating = request.form.get('rating')
    lattitude = request.form.get('lattitude')
    longitude = request.form.get('longitude')

    updatedAt = datetime.now()

    # Change from string to decimal
    tourismRating = float(tourismRating)
    lattitude = float(lattitude)
    longitude = float(longitude)
    entryPrice = int(entryPrice)

    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tourisms WHERE tourism_id = %s", (tourism_id,))
    checkTourism = cur.fetchone()

    if checkTourism is None:
        return_json = {
            "status" : 404,
            "message" : "tourism not found"
        }

        return return_json
    
    if request.files['image'].filename == '' and result[1] == "":
        tourismImageURL = ""
    elif request.files['image'].filename == '' and result[1] != "":
        tourismImageURL = result[1]
    else:
        tourismImageURL = uploadImage(tourismImage)

    # Tourism Type
    cur.execute("SELECT * FROM tourism_type WHERE tourism_type_id = %s;", (tourismTypeID,))
    tourismType = cur.fetchone()
    if tourismType is None:
        return_json = {
            "status" : 404,
            "message" : "tourism type not found"
        }

        return return_json
    
    tourismTypeName = tourismType[2]

    # Province
    cur.execute("SELECT * FROM provinces WHERE province_id = %s;", (provinceID,))
    province = cur.fetchone()

    if province is None:
        return_json = {
            "status" : 404,
            "message" : "province not found"
        }

        return return_json
    
    provinceName = province[2]

    cur.execute("""
                UPDATE tourisms SET
                    tourism_name = %s,
                    tourism_image = %s,
                    tourism_address = %s,
                    tourism_type_id = %s,
                    tourism_type = %s,
                    tourism_city = %s,
                    province_id = %s,
                    tourism_province = %s,
                    open_hour = %s,
                    close_hour = %s,
                    tourism_description = %s,
                    entry_price =  %s,
                    traveling_time = %s,
                    road_condition = %s,
                    tourism_rating = %s,
                    lattitude = %s,
                    longitude = %s,
                    updated_at = %s WHERE province_id = %s;""",
                    (tourismName,
                    tourismImageURL, 
                    tourismAddress, 
                    tourismTypeID,
                    tourismTypeName, 
                    tourismCity, 
                    provinceID, 
                    provinceName, 
                    openHour,
                    closeHour,
                    tourismDesc,
                    entryPrice,
                    travelingTime,
                    roadCondition,
                    tourismRating,
                    lattitude,
                    longitude,
                    updatedAt,
                    tourism_id,)
                )
    conn.commit()

    cur.execute("SELECT * FROM tourisms WHERE tourism_id = %s;", (tourism_id,))
    result = cur.fetchone()

    return_json = {
        "status" : 200,
        "message" : "success update tourism",
        "data" : {
            "id" : result[0],
            "image" : result[1],
            "name" : result[2],
            "address" : result[3],
            "type_id" : result[4],
            "type" : result[5],
            "city" : result[6],
            "province_id" : result[7],
            "province" : result[8],
            "open_hour" : result[9],
            "close_hour" : result[10],
            "description" : result[11],
            "entry_price" : result[12],
            "traveling_time" : result[13],
            "road_condition" : result[14],
            "rating" : result[15],
            "lattitude" : result[16],
            "longitude" : result[17],
            "created_at" : result[18],
            "updated_at" : result[19]
        }
    }

    return return_json

