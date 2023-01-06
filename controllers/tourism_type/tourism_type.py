from flask import Blueprint
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
        return_json = {
            "status" : 400,
            "message" : "tourism type already exist"
        }

        return return_json
    
    cur.execute("INSERT INTO tourism_type (tourism_type_image, tourism_type_name, created_at, updated_at) VALUES (%s, %s, %s, %s) RETURNING tourism_type_id;", (tourismTypeImageURL, tourismTypeName, createdAt, updatedAt,))
    conn.commit()

    returningID = cur.fetchone()[0]

    cur.execute("SELECT * FROM tourism_type WHERE tourism_type_id = %s", (returningID,))
    result = cur.fetchone()

    return_json = {
            "status" : 201,
            "message" : "success create tourism type",
            "data" : {
                "id" : result[0],
                "image" : result[1],
                "name" : result[2],
                "created_at" : result[3],
                "updated_at" : result[4]
            }
        }

    return return_json


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
        return_json = {
            "status" : 404,
            "message" : "tourism type not found"
        }

        return return_json

    if request.files['image'].filename == '' and result[1] == "":
        tourismTypeImageURL = ""
    elif request.files['image'].filename == '' and result[1] != "":
        tourismTypeImageURL = result[1]
    else:
        tourismTypeImageURL = uploadImage(tourismTypeImage)
    
    isTourismTypeDuplicated = checkTourismTypeDuplicated(tourismTypeName)

    if isTourismTypeDuplicated:
        return_json = {
            "status" : 400,
            "message" : "tourism type already exist"
        }

        return return_json
    
    cur.execute("UPDATE tourism_type SET tourism_type_image = %s, tourism_type_name = %s, updated_at = %s WHERE tourism_type_id = %s;", (tourismTypeImageURL, tourismTypeName, updatedAt, type_id,))
    conn.commit()

    cur.execute("SELECT * FROM tourism_type WHERE tourism_type_id = %s", (type_id,))
    updatedResult = cur.fetchone()

    return_json = {
            "status" : 200,
            "message" : "success update tourism type",
            "data" : {
                "id" : updatedResult[0],
                "image" : updatedResult[1],
                "name" : updatedResult[2],
                "created_at" : updatedResult[3],
                "updated_at" : updatedResult[4]
            }
        }

    return return_json

    
@tourism_type.route("/v1/tourism-type", methods = ['GET'])
@jwt_required()
def getAllTourismType():
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tourism_type")
    tourismType = cur.fetchall()

    result = []

    if len(tourismType) != 0:
        for item in tourismType:
            result.append({
                "id" : item[0],
                "image" : item[1],
                "name" : item[2],
                "created_at" : item[3],
                "updated_at" : item[4]
            })
    
    return_json = {
        "status" : 200,
        "message" : "success get all tourism type",
        "data" : result
    }

    return return_json

@tourism_type.route("/v1/tourism-type/<type_id>", methods = ['DELETE'])
@jwt_required()
def deleteTourismType(type_id):
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tourism_type WHERE tourism_type_id = %s;", (type_id,))
    result = cur.fetchone()

    if result is None:
        return_json = {
            "status" : 404,
            "message" : "tourism type not found"
        }

        return return_json
    
    cur.execute("DELETE FROM tourism_type WHERE tourism_type_id = %s;", (type_id,))
    conn.commit()
    
    return_json = {
        "status" : 200,
        "message" : "success delete tourism type",
        "data" : ""
    }

    return return_json

@tourism_type.route("/v1/tourism-type/<type_id>", methods = ['GET'])
@jwt_required()
def getOneTourismType(type_id):
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tourism_type WHERE tourism_type_id = %s", (type_id,))
    result = cur.fetchone()
    
    return_json = {
        "status" : 200,
        "message" : "success get all tourism type",
        "data" : {
            "id" : result[0],
            "image" : result[1],
            "name" : result[2],
            "created_at" : result[3],
            "updated_at" : result[4]
        }
    }

    return return_json


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