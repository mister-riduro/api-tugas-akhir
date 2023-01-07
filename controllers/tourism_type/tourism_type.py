from flask import Blueprint, request
from flask_cors import CORS
from flask_jwt_extended import jwt_required

from helpers import *

from datetime import datetime

tourism_type = Blueprint('tourism_type', __name__)
cors = CORS(tourism_type, resources={r"/v1/*": {"origins": "*"}})

@tourism_type.route("/v1/tourism-type", methods = ['POST'])
@jwt_required()
def createTourismType():
    tourismTypeImage = request.files['image']
    tourismTypeName = request.form.get('name')

    createdAt = datetime.now()
    updatedAt = datetime.now()

    conn = initializeDB()
    cur = conn.cursor()

    if request.files['image'].filename == '':
        tourismTypeImageURL = ""
    else:
        tourismTypeImageURL = uploadImage(tourismTypeImage)
    
    isTourismTypeDuplicated = checkTourismTypeDuplicated(tourismTypeName)

    if isTourismTypeDuplicated:
        return responseFailJSON(400, "tourism type already exist")
    
    cur.execute("INSERT INTO tourism_type (tourism_type_image, tourism_type_name, created_at, updated_at) VALUES (%s, %s, %s, %s) RETURNING tourism_type_id;", (tourismTypeImageURL, tourismTypeName, createdAt, updatedAt,))
    conn.commit()

    returningID = cur.fetchone()[0]

    cur.execute("SELECT * FROM tourism_type WHERE tourism_type_id = %s", (returningID,))
    result = cur.fetchone()

    data = insertOneData(result)

    return responseSuccessJSON(201, "success create tourism type", data)


@tourism_type.route("/v1/tourism-type/<type_id>", methods = ['PUT'])
@jwt_required()
def updateTourismType(type_id):
    tourismTypeImage = request.files['image']
    tourismTypeName = request.form.get('name')

    updatedAt = datetime.now()

    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tourism_type WHERE tourism_type_id = %s", (type_id,))
    result = cur.fetchone()

    if result is None:
        return responseFailJSON(404, "tourism type not found")

    if request.files['image'].filename == '' and result[1] == "":
        tourismTypeImageURL = ""
    elif request.files['image'].filename == '' and result[1] != "":
        tourismTypeImageURL = result[1]
    else:
        tourismTypeImageURL = uploadImage(tourismTypeImage)
    
    isTourismTypeDuplicated = checkTourismTypeDuplicated(tourismTypeName)

    if isTourismTypeDuplicated:
        return responseFailJSON(400, "tourism type already exist")
    
    cur.execute("UPDATE tourism_type SET tourism_type_image = %s, tourism_type_name = %s, updated_at = %s WHERE tourism_type_id = %s;", (tourismTypeImageURL, tourismTypeName, updatedAt, type_id,))
    conn.commit()

    cur.execute("SELECT * FROM tourism_type WHERE tourism_type_id = %s", (type_id,))
    updatedResult = cur.fetchone()

    data = insertOneData(updatedResult)

    return responseSuccessJSON(200, "success update tourism type", data)

    
@tourism_type.route("/v1/tourism-type", methods = ['GET'])
@jwt_required()
def getAllTourismType():
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tourism_type")
    tourismType = cur.fetchall()

    result = []

    if len(tourismType) != 0:
        result = insertMultipleData(tourismType)

    return responseSuccessJSON(200, "success get all tourism type", result)

@tourism_type.route("/v1/tourism-type/<type_id>", methods = ['DELETE'])
@jwt_required()
def deleteTourismType(type_id):
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tourism_type WHERE tourism_type_id = %s;", (type_id,))
    result = cur.fetchone()

    if result is None:
        return responseFailJSON(404, "tourism type not found")
    
    cur.execute("DELETE FROM tourism_type WHERE tourism_type_id = %s;", (type_id,))
    conn.commit()

    return responseSuccessJSON(200, "success delete tourism type", "")

@tourism_type.route("/v1/tourism-type/<type_id>", methods = ['GET'])
@jwt_required()
def getOneTourismType(type_id):
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tourism_type WHERE tourism_type_id = %s", (type_id,))
    result = cur.fetchone()
    
    data = insertOneData(result)

    return responseSuccessJSON(200, "success get tourism type", data)


def checkTourismTypeDuplicated(tourismTypeName):
    tourismTypeName = str(tourismTypeName)

    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tourism_type")
    result = cur.fetchall()

    cur.close()

    if len(result) == 0:
        return False
    else:
        for item in result:
            fetchedTourismType = str(item[2])

            if tourismTypeName.lower() == fetchedTourismType.lower():
                return True

        return False

def insertOneData(item):
    data = {
            "id" : item[0],
            "image" : item[1],
            "name" : item[2],
            "created_at" : item[3],
            "updated_at" : item[4]
        }

    return data

def insertMultipleData(items):
    datas = []

    for item in items:
        datas.append({
            "id" : item[0],
            "image" : item[1],
            "name" : item[2],
            "created_at" : item[3],
            "updated_at" : item[4]
        })
    
    return datas