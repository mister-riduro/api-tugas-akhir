from flask import Blueprint, jsonify
from flask_cors import CORS
from flask_jwt_extended import jwt_required

from helpers import *

from datetime import datetime


nearestEvent = Blueprint('nearestEvent', __name__)
cors = CORS(nearestEvent, resources={r"/v1/*": {"origins": "*"}})

initializeENV()

@nearestEvent.route("/v1/nearest-event", methods = ['POST'])
@jwt_required()
def createNearestEvent(): 

    eventImage = request.files['image']
    eventName = request.form.get('name')
    eventStartDate = request.form.get('start_date')
    eventEndDate = request.form.get('end_date')
    eventLocation = request.form.get('location')
    eventDescription = request.form.get('description')
    createdAt = datetime.now()
    updatedAt = datetime.now()

    conn = initializeDB()
    cur = conn.cursor()

    if request.files['image'].filename == '':
        eventImageURL = ""
    else:
        eventImageURL = uploadImage(eventImage)

    cur.execute("INSERT INTO nearest_event (event_image, event_name, event_start_date, event_end_date, event_location, event_description, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING nearest_event_id;", (eventImageURL, eventName, eventStartDate, eventEndDate, eventLocation, eventDescription, createdAt, updatedAt))
    conn.commit()
    returningID = cur.fetchone()[0]

    cur.execute("SELECT * FROM nearest_event WHERE nearest_event_id = %s;", (returningID,))
    result = cur.fetchone()

    cur.close()

    return_json = {
                "status" : 200,
                "message" : "success create nearest event",
                "data" : {
                    'id' : result[0],
                    'image' : result[1],
                    'name' : result[2],
                    'start_date' : result[3],
                    'end_date' : result[4],
                    'location' : result[5],
                    'description' : result[6],
                    'created_at' : result[7],
                    'updated_at' : result[8]
                }
            }

    return return_json

@nearestEvent.route("/v1/nearest-event/<event_id>", methods = ['PUT'])
@jwt_required()
def updateNearestEvent(event_id):
    conn = initializeDB()
    cur = conn.cursor()

    eventImage = request.files['image']
    eventName = request.form.get('name')
    eventStartDate = request.form.get('start_date')
    eventEndDate = request.form.get('end_date')
    eventLocation = request.form.get('location')
    eventDescription = request.form.get('description')
    updatedAt = datetime.now()

    cur.execute("SELECT * FROM nearest_event WHERE nearest_event_id = %s;", (event_id,))
    result = cur.fetchone()

    if result is None:
        return_json = {
                "status" : 400,
                "message" : "event not found",
                "data" : ""
            }
        return return_json

    if request.files['image'].filename == '' and result[1] == "":
        eventImageURL = ""
    elif request.files['image'].filename == '' and result[1] != "":
        eventImageURL = result[1]
    else:
        eventImageURL = uploadImage(eventImage)
    
    cur.execute("UPDATE nearest_event SET event_image = %s, event_name = %s, event_start_date = %s, event_end_date = %s, event_location = %s, event_description = %s, updated_at = %s WHERE nearest_event_id = %s;", (eventImageURL, eventName, eventStartDate, eventEndDate, eventLocation, eventDescription, updatedAt, event_id))
    conn.commit()

    if cur.rowcount != 1:
        return_json = {
                "status" : 500,
                "message" : "error update data",
            }
        return return_json
    
    cur.execute("SELECT * FROM nearest_event WHERE nearest_event_id = %s;", (event_id,))
    resUpdated = cur.fetchone()

    return_json = {
            "status" : 200,
            "message" : "event successfully updated",
            "data" : {
                'id' : resUpdated[0],
                'image' : resUpdated[1],
                'name' : resUpdated[2],
                'start_date' : resUpdated[3],
                'end_date' : resUpdated[4],
                'location' : resUpdated[5],
                'description' : resUpdated[6],
                'created_at' : resUpdated[7],
                'updated_at' : resUpdated[8]
            }
    }
    
    return return_json

@nearestEvent.route("/v1/nearest-event/<event_id>", methods = ['GET'])
@jwt_required()
def getOneNearestEvent(event_id):
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM nearest_event WHERE nearest_event_id = %s;", (event_id,))
    conn.commit()
    result = cur.fetchone()

    if result is None:
        return_json = {
                "status" : 400,
                "message" : "event not found",
                "data" : ""
            }
        return return_json
    
    return_json = {
        "status" : 200,
        "message" : "success get nearest event",
        "data" : {
            'id' : result[0],
            'image' : result[1],
            'name' : result[2],
            'start_date' : result[3],
            'end_date' : result[4],
            'location' : result[5],
            'description' : result[6],
            'created_at' : result[7],
            'updated_at' : result[8]
        }
    }

    return return_json

@nearestEvent.route("/v1/nearest-event/<event_id>", methods = ['DELETE'])
@jwt_required()
def deleteNearestEvent(event_id):
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM nearest_event WHERE nearest_event_id = %s;", (event_id,))
    result = cur.fetchone()

    if result is None:
        return_json = {
                "status" : 400,
                "message" : "event not found",
                "data" : ""
            }
        return return_json

    cur.execute("DELETE FROM nearest_event WHERE nearest_event_id = %s", (event_id,))
    conn.commit()

    return_json = {
            "status" : 200,
            "message" : "event deleted",
            "data" : ""
        }
    return return_json
    

@nearestEvent.route("/v1/nearest-event", methods = ['GET'])
@jwt_required()
def getAllNearestEvent():
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM nearest_event;")
    events = cur.fetchall()
    cur.close()

    output = []

    for item in events:
        output.append({
            'id' : item[0],
            'image' : item[1],
            'name' : item[2],
            'start_date' : item[3],
            'end_date' : item[4],
            'location' : item[5],
            'description' : item[6],
            'created_at' : item[7],
            'updated_at' : item[8]
        })

    return_json = {
                "status" : 200,
                "message" : "success get all datas",
                "data" : output
            }
            
    return return_json



