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
    tourismType = request.form.get('tourism_type')
    tourismCity = request.form.get('city')
    provinceName = request.form.get('province_name')
    openHour = request.form.get('open_hour')
    closeHour = request.form.get('close_hour')
    tourismDesc = request.form.get('description')
    entryPrice = request.form.get('entry_price')
    travelingTime = request.form.get('traveling_time')
    roadCondition = request.form.get('road_condition')

    tourismRating = request.form.get('rating')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    createdAt = datetime.now()
    updatedAt = datetime.now()

    # Change from string to decimal
    tourismRating = float(tourismRating)
    latitude = float(latitude)
    longitude = float(longitude)
    entryPrice = int(entryPrice)

    conn = initializeDB()
    cur = conn.cursor()

    if request.files['image'].filename == '':
        tourismImageURL = ""
    else:
        tourismImageURL = uploadImage(tourismImage)

    cur.execute("""
                INSERT INTO tourisms (
                    tourism_name,
                    tourism_image,
                    tourism_address,
                    tourism_type,
                    tourism_city,
                    province_name
                    open_hour,
                    close_hour,
                    tourism_description,
                    entry_price,
                    traveling_time,
                    road_condition,
                    tourism_rating,
                    latitude,
                    longitude,
                    created_at,
                    updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING tourism_id;""",
                    (tourismName,
                    tourismImageURL, 
                    tourismAddress, 
                    tourismType,
                    tourismCity, 
                    provinceName, 
                    openHour,
                    closeHour,
                    tourismDesc,
                    entryPrice,
                    travelingTime,
                    roadCondition,
                    tourismRating,
                    latitude,
                    longitude,
                    createdAt,
                    updatedAt,)
                )
    conn.commit()
    returningID = cur.fetchone()[0]

    cur.execute("SELECT * FROM tourisms WHERE tourism_id = %s;", (returningID,))
    result = cur.fetchone()

    facilities = []
    data = insertOneData(result, facilities)

    return responseSuccessJSON(201, "success create tourism", data)

@tourisms.route("/v1/tourisms/<tourism_id>", methods = ['GET'])
@jwt_required()
def getOneTourism(tourism_id):
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tourisms WHERE tourism_id = %s;", (tourism_id,))
    result = cur.fetchone()

    if result is None:
        return responseFailJSON(404, "tourism not found")

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

    data = insertOneData(result, facilities)

    return responseSuccessJSON(200, "success get tourism", data)

@tourisms.route("/v1/tourisms", methods = ['GET'])
@jwt_required()
def getAllTourism():
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tourisms;")
    tourism = cur.fetchall()

    result = []
    result = insertMultipleData(tourism, cur)

    return responseSuccessJSON(200, "success get all tourism", result)

@tourisms.route("/v1/tourisms/p", methods = ['GET'])
@jwt_required()
def getTourismsByProvince():
    conn = initializeDB()
    cur = conn.cursor()

    provinceName = request.json['province_name']

    cur.execute("SELECT * FROM tourisms WHERE province_name = %s;", (provinceName))
    tourism = cur.fetchall()

    result = []
    result = insertMultipleData(tourism, cur)

    return responseSuccessJSON(200, "success get all tourism based on province", result)

@tourisms.route("/v1/tourisms/<tourism_id>", methods = ['DELETE'])
@jwt_required()
def deleteTourism(tourism_id):
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tourisms WHERE tourism_id = %s;", (tourism_id,))
    result = cur.fetchone()

    if result is None:
        return responseFailJSON(404, "tourism not found")

    cur.execute("DELETE FROM tourisms WHERE tourism_id = %s;", (tourism_id,))
    conn.commit()
    

    return responseSuccessJSON(200, "success delete tourism", "")

@tourisms.route("/v1/tourisms/<tourism_id>", methods = ['PUT'])
@jwt_required()
def updateTourism(tourism_id):
    tourismName = request.form.get('name')
    tourismImage = request.files['image']
    tourismAddress = request.form.get('address')
    tourismType = request.form.get('tourism_type')
    tourismCity = request.form.get('city')
    provinceName = request.form.get('province_name')
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
    latitude = float(lattitude)
    longitude = float(longitude)
    entryPrice = int(entryPrice)

    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tourisms WHERE tourism_id = %s", (tourism_id,))
    checkTourism = cur.fetchone()

    if checkTourism is None:
        return responseFailJSON(404, "tourism not found")
    
    if request.files['image'].filename == '' and result[1] == "":
        tourismImageURL = ""
    elif request.files['image'].filename == '' and result[1] != "":
        tourismImageURL = result[1]
    else:
        tourismImageURL = uploadImage(tourismImage)

    cur.execute("""
                UPDATE tourisms SET
                    tourism_name = %s,
                    tourism_image = %s,
                    tourism_address = %s,
                    tourism_type = %s,
                    tourism_city = %s,
                    province_name = %s,
                    open_hour = %s,
                    close_hour = %s,
                    tourism_description = %s,
                    entry_price =  %s,
                    traveling_time = %s,
                    road_condition = %s,
                    tourism_rating = %s,
                    latitude = %s,
                    longitude = %s,
                    updated_at = %s WHERE tourism_id = %s;""",
                    (tourismName,
                    tourismImageURL, 
                    tourismAddress, 
                    tourismType,
                    tourismCity, 
                    provinceName, 
                    openHour,
                    closeHour,
                    tourismDesc,
                    entryPrice,
                    travelingTime,
                    roadCondition,
                    tourismRating,
                    latitude,
                    longitude,
                    updatedAt,
                    tourism_id,)
                )
    conn.commit()

    cur.execute("SELECT * FROM tourisms WHERE tourism_id = %s;", (tourism_id,))
    result = cur.fetchone()

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

    data = insertOneData(result, facilities)

    return responseSuccessJSON(200, "success update tourism", data)


def insertOneData(item, facilities):
    data = {
            "id" : item[0],
            "image" : item[1],
            "name" : item[2],
            "address" : item[3],
            "type" : item[4],
            "city" : item[5],
            "province_name" : item[6],
            "open_hour" : item[7],
            "close_hour" : item[8],
            "description" : item[9],
            "entry_price" : item[10],
            "facilities" : facilities,
            "traveling_time" : item[11],
            "road_condition" : item[12],
            "rating" : item[13],
            "lattitude" : item[14],
            "longitude" : item[15],
            "created_at" : item[16],
            "updated_at" : item[17]
        }

    return data


def insertMultipleData(items, cur):
    datas = []

    for item in items:
        cur.execute("SELECT tfacilities.tfacilities_id, tfacilities.facilities_name FROM tourisms JOIN tfacilities ON tourisms.tourism_id = %s", (item[0],))
        fetchedFacilties = cur.fetchall()

        facilities = []

        if len(fetchedFacilties) != 0:
            for facil in fetchedFacilties:
                facilities.append({
                    "id" : facil[0],
                    "name" : facil[1]
                })

        datas.append({
            "id" : item[0],
            "image" : item[1],
            "name" : item[2],
            "address" : item[3],
            "type" : item[4],
            "city" : item[5],
            "province_name" : item[6],
            "open_hour" : item[7],
            "close_hour" : item[8],
            "description" : item[9],
            "entry_price" : item[10],
            "facilities" : facilities,
            "traveling_time" : item[11],
            "road_condition" : item[12],
            "rating" : item[13],
            "lattitude" : item[14],
            "longitude" : item[15],
            "created_at" : item[16],
            "updated_at" : item[17]
        })
    
    return datas