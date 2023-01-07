from flask import Blueprint, request
from flask_cors import CORS
from flask_jwt_extended import jwt_required

from helpers import *

from datetime import datetime

provinces = Blueprint('provinces', __name__)
cors = CORS(provinces, resources={r"/v1/*": {"origins": "*"}})

initializeENV()

@provinces.route("/v1/provinces", methods=['GET'])
@jwt_required()
def getAllProvinces():
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM provinces")
    provinces = cur.fetchall()

    result = []

    if len(provinces) != 0:
        for item in provinces:
            result.append({
                'id' : item[0],
                'image' : item[1],
                'name' : item[2],
                'created_at' : item[3],
                'updated_at' : item[4]
            })

    return responseSuccessJSON(200, "success get all provinces", result)

@provinces.route("/v1/provinces/<province_id>", methods=['GET'])
@jwt_required()
def getOneProvinces(province_id):
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM provinces WHERE province_id = %s;", (province_id,))
    result = cur.fetchone()

    if result is None:
        return responseFailJSON(404, "province not found")

    data = {
        'id' : result[0],
        'image' : result[1],
        'name' : result[2],
        'created_at' : result[3],
        'updated_at' : result[4]
    }

    return responseSuccessJSON(200, "success get province", data)

@provinces.route("/v1/provinces", methods = ['POST'])
@jwt_required()
def createProvinces():

    provinceImage = request.files['image']
    provinceName = request.form.get('name')
    createdAt = datetime.now()
    updatedAt = datetime.now()

    conn = initializeDB()
    cur = conn.cursor()

    if request.files['image'].filename == '':
        provinceImageURL = ""
    else:
        provinceImageURL = uploadImage(provinceImage)
    
    isDuplicate = checkDuplicate(provinceName)
    if isDuplicate:
        return responseFailJSON(400, "province already exist")

    cur.execute("INSERT INTO provinces (province_image, province_name, created_at, updated_at) VALUES (%s, %s, %s, %s) RETURNING province_id;", (provinceImageURL, provinceName, createdAt, updatedAt))
    conn.commit()
    returningID = cur.fetchone()[0]

    cur.execute("SELECT * FROM provinces WHERE province_id = %s;", (returningID,))
    result = cur.fetchone()

    cur.close()

    data = {
        'id' : result[0],
        'image' : result[1],
        'name' : result[2],
        'created_at' : result[3],
        'updated_at' : result[4]
    }

    return responseSuccessJSON(201, "success create province", data)

def checkDuplicate(provinceName):
    conn = initializeDB()
    cur = conn.cursor()

    provinceName = str(provinceName)

    cur.execute("SELECT * FROM provinces")
    result = cur.fetchall()

    cur.close()

    if len(result) == 0:
        return False
    else:
        for item in result:
            fetchedProvince = str(item[2])

            if provinceName.lower() == fetchedProvince.lower():
                return True

        return False


@provinces.route("/v1/provinces/<province_id>", methods = ['PUT'])
@jwt_required()
def updateProvinces(province_id):

    provinceImage = request.files['image']
    provinceName = request.form.get('name')
    updatedAt = datetime.now()

    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM provinces WHERE province_id = %s;", (province_id,))
    result = cur.fetchone()

    if result is None:
        return responseFailJSON(400, "province not found")

    if request.files['image'].filename == '' and result[1] == "":
        provinceImageURL = ""
    elif request.files['image'].filename == '' and result[1] != "":
        provinceImageURL = result[1]
    else:
        provinceImageURL = uploadImage(provinceImage)


    cur.execute("UPDATE provinces SET province_image = %s, province_name = %s, updated_at = %s WHERE province_id = %s;", (provinceImageURL, provinceName, updatedAt, province_id,))
    conn.commit()

    cur.execute("SELECT * FROM provinces WHERE province_id = %s;", (province_id,))
    updatedResult = cur.fetchone()

    cur.close()

    data = {
        'id' : updatedResult[0],
        'image' : updatedResult[1],
        'name' : updatedResult[2],
        'created_at' : updatedResult[3],
        'updated_at' : updatedResult[4]
    }

    return responseSuccessJSON(200, "success update province", data)

@provinces.route("/v1/provinces/<province_id>", methods = ['DELETE'])
@jwt_required()
def deleteProvinces(province_id):
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM provinces WHERE province_id = %s;", (province_id,))
    result = cur.fetchone()

    if result is None:
        return responseFailJSON(400, "province not found")


    cur.execute("DELETE FROM provinces WHERE province_id = %s;", (province_id,))
    conn.commit()

    cur.close()

    return responseSuccessJSON(200, "success delete province", "")