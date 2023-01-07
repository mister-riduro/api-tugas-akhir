from flask import Blueprint, jsonify, request
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

    data = insertOneData(result)

    return responseSuccessJSON(201, "success create nearest event", data)

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
        return responseFailJSON(404, "event not found")

    if request.files['image'].filename == '' and result[1] == "":
        eventImageURL = ""
    elif request.files['image'].filename == '' and result[1] != "":
        eventImageURL = result[1]
    else:
        eventImageURL = uploadImage(eventImage)
    
    cur.execute("UPDATE nearest_event SET event_image = %s, event_name = %s, event_start_date = %s, event_end_date = %s, event_location = %s, event_description = %s, updated_at = %s WHERE nearest_event_id = %s;", (eventImageURL, eventName, eventStartDate, eventEndDate, eventLocation, eventDescription, updatedAt, event_id))
    conn.commit()

    if cur.rowcount != 1:
        return responseFailJSON(500, "error update data")
    
    cur.execute("SELECT * FROM nearest_event WHERE nearest_event_id = %s;", (event_id,))
    resUpdated = cur.fetchone()

    data = insertOneData(resUpdated)
    
    return responseSuccessJSON(200, "success update data", data)

@nearestEvent.route("/v1/nearest-event/<event_id>", methods = ['GET'])
@jwt_required()
def getOneNearestEvent(event_id):
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM nearest_event WHERE nearest_event_id = %s;", (event_id,))
    conn.commit()
    result = cur.fetchone()

    if result is None:
        return responseFailJSON(404, "event not found")

    data = insertOneData(result)

    return responseSuccessJSON(200, "success get nearest event", data)

@nearestEvent.route("/v1/nearest-event/<event_id>", methods = ['DELETE'])
@jwt_required()
def deleteNearestEvent(event_id):
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM nearest_event WHERE nearest_event_id = %s;", (event_id,))
    result = cur.fetchone()

    if result is None:
        return responseFailJSON(404, "event not found")

    cur.execute("DELETE FROM nearest_event WHERE nearest_event_id = %s", (event_id,))
    conn.commit()

    return responseSuccessJSON(200, "success delete event", "")
    

@nearestEvent.route("/v1/nearest-event", methods = ['GET'])
@jwt_required()
def getAllNearestEvent():
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM nearest_event;")
    events = cur.fetchall()
    cur.close()

    output = []

    if len(events) != 0:
        output = insertMultipleData(events)
            
    return responseSuccessJSON(200, "success get all datas", output)


def insertOneData(item):
    data = {
        'id' : item[0],
        'image' : item[1],
        'name' : item[2],
        'start_date' : item[3],
        'end_date' : item[4],
        'location' : item[5],
        'description' : item[6],
        'created_at' : item[7],
        'updated_at' : item[8]
    }

    return data

def insertMultipleData(items):
    datas = []

    for item in items:
        datas.append({
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
    
    return datas
