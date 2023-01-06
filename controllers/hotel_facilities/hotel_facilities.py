from flask import Blueprint
from flask_cors import CORS
from flask_jwt_extended import jwt_required

from helpers import *

from datetime import datetime

hotelFacilities = Blueprint('hotelFacilities', __name__)
cors = CORS(hotelFacilities, resources={r"/v1/*": {"origins": "*"}})

initializeENV()
@hotelFacilities.route("/v1/hotel-facilities", methods = ['POST'])
@jwt_required()
def createHotelFacilities():
    facilitiesName = request.form.get('name')
    facilitiesImage = request.files['image']
    hotelID = request.form.get('hotel_id')
    createdAt = datetime.now()
    updatedAt = datetime.now()

    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM hotels WHERE hotel_id = %s;", (hotelID,))
    hotelExist = cur.fetchone()

    if hotelExist is None:
        return responseFailJSON(404, "hotel not found")

    isFacilitiesDuplicated = checkFacilitiesDuplicated(facilitiesName)

    if isFacilitiesDuplicated:
        return responseFailJSON(400, "facilities already exist")
    
    if request.files['image'].filename == '':
        facilitiesImageURL = ""
    else:
        facilitiesImageURL = uploadImage(facilitiesImage)
    
    cur.execute("INSERT INTO hfacilities (hotel_id, facilities_name, facilities_image, created_at, updated_at) VALUES(%s, %s, %s, %s, %s) RETURNING hfacilities_id;", (hotelID, facilitiesName, facilitiesImageURL, createdAt, updatedAt))
    conn.commit()

    returningID = cur.fetchone()[0]

    cur.execute("SELECT * FROM hfacilities WHERE hfacilities_id = %s;", (returningID,))
    result = cur.fetchone()

    data = {
            "id" : result[0],
            "hotel_id" : result[1],
            "name" : result[2],
            "image" : result[3],
            "created_at" : result[4],
            "updated_at" : result[5]
        }
    
    return responseSuccessJSON(201, "success create facilities", data)


def checkFacilitiesDuplicated(facilitiesName):
    facilitiesName = str(facilitiesName)

    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM hfacilities")
    result = cur.fetchall()

    cur.close()

    if len(result) == 0:
        return False
    else:
        for item in result:
            fetchedFacilities = str(item[1])

            if facilitiesName.lower() == fetchedFacilities.lower():
                return True

        return False
        
@hotelFacilities.route("/v1/hotel-facilities", methods = ['GET'])
@jwt_required()
def getAllHotelFacilities():
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM hfacilities")
    facilities = cur.fetchall()

    result = []

    if len(facilities) != 0:
        for item in facilities:
            result.append({
                'id' : item[0],
                'hotel_id' : item[1],
                'name' : item[2],
                'image' : item[3],
                'created_at' : item[4],
                'updated_at' : item[5]
            })

    return responseSuccessJSON(200, "success get all facilities", result)

@hotelFacilities.route("/v1/hotel-facilities/<facil_id>", methods = ['PUT'])
@jwt_required() 
def updateHotelFacilities(facil_id):
    facilitiesName = request.form.get('name')
    facilitiesImage = request.files['image']
    hotelID = request.form.get('hotel_id')
    updatedAt = datetime.now()

    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM hfacilities WHERE hfacilities_id = %s;", (facil_id,))
    result = cur.fetchone()

    if result is None:
        return responseFailJSON(404, "facilities not found")
    
    cur.execute("SELECT * FROM hotels WHERE hotel_id = %s;", (hotelID,))
    tourismExist = cur.fetchone()

    if tourismExist is None:
        return responseFailJSON(404, "hotel not found")

    if request.files['image'].filename == '' and result[1] == "":
        facilitiesImageURL = ""
    elif request.files['image'].filename == '' and result[1] != "":
        facilitiesImageURL = result[1]
    else:
        facilitiesImageURL = uploadImage(facilitiesImage)
    
    cur.execute("UPDATE hfacilities SET facilities_image = %s, facilities_name = %s, hotel_id = %s, updated_at = %s WHERE hfacilities_id = %s;", (facilitiesImageURL, facilitiesName, hotelID, updatedAt))
    conn.commit()

    cur.execute("SELECT * FROM hfacilities WHERE hfacilities_id = %s;", (facil_id,))
    updatedResult = cur.fetchone()

    data = {
                    "id" : updatedResult[0],
                    "hotel_id" : updatedResult[1],
                    "name" : updatedResult[2],
                    "image" : updatedResult[3],
                    "created_at" : updatedResult[4],
                    "updated_at" : updatedResult[5]
                }

    return responseSuccessJSON(200, "success update facilities", data)


@hotelFacilities.route("/v1/hotel-facilities/<facil_id>", methods = ['DELETE'])
@jwt_required()
def deleteHotelFacilities(facil_id):
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM hfacilities WHERE facilities_id = %s;", (facil_id,))
    result = cur.fetchone()

    if result is None:
        responseFailJSON(404, "facilities not found")
    
    cur.execute("DELETE FROM hfacilities WHERE hfacilities_id = %s;", (facil_id,))
    conn.commit()

    return responseSuccessJSON(200, "success delete facilities", "")