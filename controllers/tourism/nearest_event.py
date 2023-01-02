from flask import Blueprint, jsonify
from flask_cors import CORS
from flask_jwt_extended import jwt_required

from helpers import *

nearestEvent = Blueprint('nearestEvent', __name__)
cors = CORS(nearestEvent, resources={r"/v1/*": {"origins": "*"}})

initializeENV()

@nearestEvent.route("/v1/nearest-event", methods = ['GET', 'POST'])
@jwt_required()
def nearestEvent():
    if request.method == 'GET':
        getNearestEvent()
    elif request.method == 'POST':
        createNearestEvent()


def createNearestEvent():
    eventImage = request.files('image')
    eventName = request.form.get('name')
    eventDate = request.form.get('date')
    eventLocation = request.form.get('location')
    eventDescription = request.form.get('description')

    conn = initializeDB()
    cur = conn.cursor()

    eventImageURL = uploadImage(eventImage)

    cur.execute("INSERT INTO nearest_event VALUES (default, %s, %s, %s, %s, %s);", (eventImageURL, eventName, eventDate, eventLocation, eventDescription))
    conn.commit()
    returningID = cur.fetchone()[0]

    cur.execute("SELECT * FROM nearest_event WHERE id = %d;", (returningID,))
    result = cur.fetchone()

    cur.close()

    return_json = {
                "status" : 200,
                "message" : "success create nearest event",
                "data" : result
            }

    return return_json

def getNearestEvent():
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
            'date' : item[3],
            'location' : item[4],
            'description' : item[5],
            'created_at' : item[6],
            'updated_at' : item[7]
        })

    return_json = {
                "status" : 200,
                "message" : "success get all datas",
                "data" : output
            }
            
    return return_json



