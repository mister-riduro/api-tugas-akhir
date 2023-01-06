from flask import Blueprint
from flask_cors import CORS
from flask_jwt_extended import jwt_required

from helpers import *

from datetime import datetime

tourismFacilities = Blueprint('tourismFacilities', __name__)
cors = CORS(tourismFacilities, resources={r"/v1/*": {"origins": "*"}})

initializeENV()

@tourismFacilities.route("/v1/tourism-facilities", methods = ['POST'])
@jwt_required()
def createTourismFacilities():
    facilitiesName = request.json['name']
    tourismID = request.json['tourism_id']
    createdAt = datetime.now()
    updatedAt = datetime.now()

    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tourisms WHERE tourism_id = %s;", (tourismID,))
    tourismExist = cur.fetchone()

    if tourismExist is None:
        return_json = {
                "status" : 404,
                "message" : "tourism not found",
            }
        return return_json

    isFacilitiesDuplicated = checkFacilitiesDuplicated(facilitiesName)

    if isFacilitiesDuplicated:
        return_json = {
                "status" : 400,
                "message" : "facilities already exist",
            }
        return return_json
    
    cur.execute("INSERT INTO tfacilities (tourism_id, facilities_name,created_at, updated_at) VALUES(%s, %s, %s, %s) RETURNING tfacilities_id;", (tourismID, facilitiesName, createdAt, updatedAt))
    conn.commit()

    returningID = cur.fetchone()[0]

    cur.execute("SELECT * FROM tfacilities WHERE tfacilities_id = %s;", (returningID,))
    result = cur.fetchone()

    return_json = {
                "status" : 201,
                "message" : "success create facilities",
                "data" : {
                    "id" : result[0],
                    "tourism_id" : result[1],
                    "name" : result[2],
                    "created_at" : result[3],
                    "updated_at" : result[4]
                }
            }
    return return_json


def checkFacilitiesDuplicated(facilitiesName):
    facilitiesName = str(facilitiesName)

    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tfacilities")
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
        
@tourismFacilities.route("/v1/tourism-facilities", methods = ['GET'])
@jwt_required()
def getAllTourismFacilities():
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tfacilities")
    facilities = cur.fetchall()

    result = []

    if len(facilities) != 0:
        for item in facilities:
            result.append({
                'id' : item[0],
                'tourism_id' : item[1],
                'name' : item[2],
                'created_at' : item[3],
                'updated_at' : item[4]
            })

    return_json = {
        'status' : 200,
        'message' : "success get all facilities",
        'data' : result
    }

    return return_json

@tourismFacilities.route("/v1/tourism-facilities/<facil_id>", methods = ['PUT'])
@jwt_required() 
def updateTourismFacilities(facil_id):
    facilitiesName = request.json['name']
    tourismID = request.json['tourism_id']
    updatedAt = datetime.now()

    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tfacilities WHERE tfacilities_id = %s;", (facil_id,))
    result = cur.fetchone()

    if result is None:
        return_json = {
            "status" : 404,
            "message" : "facilities not found"
        }
    
    cur.execute("SELECT * FROM tourisms WHERE tourism_id = %s;", (tourismID,))
    tourismExist = cur.fetchone()

    if tourismExist is None:
        return_json = {
                "status" : 404,
                "message" : "tourism not found",
            }
        return return_json
    
    cur.execute("UPDATE tfacilities SET facilities_name = %s, tourism_id = %s, updated_at = %s WHERE tfacilities_id = %s;", (facilitiesName, tourismID, updatedAt))
    conn.commit()

    cur.execute("SELECT * FROM tfacilities WHERE tfacilities_id = %s;", (facil_id,))
    updatedResult = cur.fetchone()

    return_json = {
                "status" : 200,
                "message" : "success update facilities",
                "data" : {
                    "id" : updatedResult[0],
                    "tourism_id" : updatedResult[1],
                    "name" : updatedResult[2],
                    "created_at" : updatedResult[3],
                    "updated_at" : updatedResult[4]
                }
            }
    return return_json


@tourismFacilities.route("/v1/tourism-facilities/<facil_id>", methods = ['DELETE'])
@jwt_required()
def deleteTourismFacilities(facil_id):
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tfacilities WHERE facilities_id = %s;", (facil_id,))
    result = cur.fetchone()

    if result is None:
        return_json = {
            "status" : 404,
            "message" : "facilities not found"
        }
    
    cur.execute("DELETE FROM tfacilities WHERE tfacilities_id = %s;", (facil_id,))
    conn.commit()

    return_json = {
                "status" : 200,
                "message" : "success create facilities",
                "data" : ""
            }
    return return_json