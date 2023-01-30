from flask import Blueprint, request
from flask_cors import CORS
from flask_jwt_extended import jwt_required

from helpers import *

from datetime import datetime

tourismRoutes = Blueprint('tourismFacilities', __name__)
cors = CORS(tourismRoutes, resources={r"/v1/*": {"origins": "*"}})

initializeENV()

@tourismRoutes.route("/v1/tourism-routes", methods = ['POST'])
@jwt_required()
def createTourismRoutes():
    routesDesc = request.json['routes_desc']
    routesPosition = request.json['request_position']
    tourismID = request.json['tourism_id']
    createdAt = datetime.now()
    updatedAt = datetime.now()

    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tourisms WHERE tourism_id = %s;", (tourismID,))
    tourismExist = cur.fetchone()

    if tourismExist is None:
        return responseFailJSON(404, "tourism not found")
    
    cur.execute("INSERT INTO routes (r_tourism_id, routes_desc, position, created_at, updated_at) VALUES(%s, %s, %s, %s, %s) RETURNING routes_id;", (tourismID, routesDesc, routesPosition, createdAt, updatedAt))
    conn.commit()

    returningID = cur.fetchone()[0]

    cur.execute("SELECT * FROM routes WHERE routes_id = %s", (returningID))
    result = cur.fetchone()

    data = insertOneData(result)

    return responseSuccessJSON(201, "success create routes", data)

@tourismRoutes.route("/v1/tourism-routes/t/<tourism_id>", methods = ['GET'])
@jwt_required()
def getRoutesByTourism(tourism_id):
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tourisms WHERE tourism_id = %s;", (tourism_id,))
    tourismExist = cur.fetchone()

    if tourismExist is None:
        return responseFailJSON(404, "tourism not found")
    
    cur.execute("SELECT * FROM routes WHERE r_tourism_id = %s;", (tourism_id,))
    routes = cur.fetchall()

    if len(routes) != 0:
        result = []
        result = insertMultipleData(routes)
    else:
        return responseFailJSON(404, "tourism not found")
    

    return responseSuccessJSON(200, "success get all tourism routes by tourism_id", result)
    
@tourismRoutes.route("/v1/tourism-routes/<routes_id>", methods = ['PUT'])
@jwt_required()
def updateTourismRoutes(routes_id):
    routesDesc = request.json['routes_desc']
    routesPosition = request.json['request_position']
    tourismID = request.json['tourism_id']
    updatedAt = datetime.now()

    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tourisms WHERE tourism_id = %s;", (tourismID,))
    tourismExist = cur.fetchone()

    if tourismExist is None:
        return responseFailJSON(404, "tourism not found")
    
    cur.execute("SELECT * FROM routes WHERE routes_id = %s;", (routes_id,))
    routesExist = cur.fetchone()

    if routesExist is None:
        return responseFailJSON(404, "routes not found")

    cur.execute("UPDATE routes SET routes_desc = %s, r_tourism_id = %s, position = %s, updated_at = %s WHERE routes_id = %s;", (routesDesc, tourismID, routesPosition, updatedAt, routes_id))
    conn.commit()

    cur.execute("SELECT * FROM routes WHERE routes_id = %s;", (routes_id,))
    updatedResult = cur.fetchone()

    data = insertOneData(updatedResult)

    return responseSuccessJSON(200, "success update routes", data)

@tourismRoutes.route("/v1/tourism-routes/<routes_id>", methods = ['DELETE'])
@jwt_required()
def deleteTourismRoutes(routes_id):
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM routes WHERE routes_id = %s;", (routes_id,))
    routesExist = cur.fetchone()

    if routesExist is None:
        return responseFailJSON(404, "routes not found")
    
    cur.execute("DELETE FROM routes WHERE routes_id = %s;", (routes_id,))
    conn.commit()

    return responseSuccessJSON(200, "success delete routes", "")

def insertOneData(item):
    data = {
            'id' : item[0],
            'tourism_id' : item[1],
            'routes_desc' : item[2],
            'position' : item[3],
            'created_at' : item[4],
            'updated_at' : item[5]
        }

    return data

def insertMultipleData(items):
    datas = []

    if len(items) != 0:
        for item in items:
            datas.append({
                'id' : item[0],
                'tourism_id' : item[1],
                'routes_desc' : item[2],
                'position' : item[3],
                'created_at' : item[4],
                'updated_at' : item[5]
            })
    
    return datas