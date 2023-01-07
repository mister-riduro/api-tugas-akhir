from flask import Blueprint, request
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
        return responseFailJSON(404, "tourism not found")

    isFacilitiesDuplicated = checkFacilitiesDuplicated(facilitiesName)

    if isFacilitiesDuplicated:
        return responseFailJSON(400, "facilities already exist")
    
    cur.execute("INSERT INTO tfacilities (tourism_id, facilities_name,created_at, updated_at) VALUES(%s, %s, %s, %s) RETURNING tfacilities_id;", (tourismID, facilitiesName, createdAt, updatedAt))
    conn.commit()

    returningID = cur.fetchone()[0]

    cur.execute("SELECT * FROM tfacilities WHERE tfacilities_id = %s;", (returningID,))
    result = cur.fetchone()

    data = insertOneData(result)

    return responseSuccessJSON(201, "success create facilities", data)
        
@tourismFacilities.route("/v1/tourism-facilities", methods = ['GET'])
@jwt_required()
def getAllTourismFacilities():
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tfacilities")
    facilities = cur.fetchall()

    result = []

    if len(facilities) != 0:
        result = insertMultipleData(facilities)

    return responseSuccessJSON(200, "success get all facilities", result)

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
        return responseFailJSON(404, "facilities not found")
    
    cur.execute("SELECT * FROM tourisms WHERE tourism_id = %s;", (tourismID,))
    tourismExist = cur.fetchone()

    if tourismExist is None:
        return responseFailJSON(404, "tourism not found")
    
    cur.execute("UPDATE tfacilities SET facilities_name = %s, tourism_id = %s, updated_at = %s WHERE tfacilities_id = %s;", (facilitiesName, tourismID, updatedAt))
    conn.commit()

    cur.execute("SELECT * FROM tfacilities WHERE tfacilities_id = %s;", (facil_id,))
    updatedResult = cur.fetchone()

    data = insertOneData(updatedResult)

    return responseSuccessJSON(200, "success update facilities", data)


@tourismFacilities.route("/v1/tourism-facilities/<facil_id>", methods = ['DELETE'])
@jwt_required()
def deleteTourismFacilities(facil_id):
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tfacilities WHERE facilities_id = %s;", (facil_id,))
    result = cur.fetchone()

    if result is None:
        return responseFailJSON(404, "facilities not found")
    
    cur.execute("DELETE FROM tfacilities WHERE tfacilities_id = %s;", (facil_id,))
    conn.commit()

    return responseSuccessJSON(200, "success delete facilities", "")

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

def insertOneData(item):
    data = {
            'id' : item[0],
            'tourism_id' : item[1],
            'name' : item[2],
            'created_at' : item[3],
            'updated_at' : item[4]
        }

    return data

def insertMultipleData(items):
    datas = []

    for item in items:
        datas.append({
            'id' : item[0],
            'tourism_id' : item[1],
            'name' : item[2],
            'created_at' : item[3],
            'updated_at' : item[4]
        })
    
    return datas