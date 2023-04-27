from flask import Blueprint, jsonify, request, json
from flask_cors import CORS
from helpers import *
from sklearn.preprocessing import MinMaxScaler

from flask_jwt_extended import jwt_required

import joblib
import numpy as np

recommendation = Blueprint('recommendation', __name__)
cors = CORS(recommendation, resources={r"/v1/*": {"origins": "*"}})

MAX_FACIL_RATE = 10.5
MIN_FACIL_RATE = 0.0
MAX_HOTEL_RATE = 5.0
MIN_HOTEL_RATE = 0.0

kmeans = joblib.load('D:/College/final-project/api_ta/controllers/recommendation/kmeans.joblib')
print(kmeans)
scaler = joblib.load('D:/College/final-project/api_ta/controllers/recommendation/scaler.joblib')

@recommendation.route("/v1/recommend", methods = ['POST'])
def recommendHotels():
    facilities = request.json['facilities']
    hotelRating = request.json['hotel_rating']
    # hotelCity = request.json['hotel_city']

    score = calculateRate(facilities)
    res = recommend(score, hotelRating)

    # conn = initializeDB()
    # cur = conn.cursor()

    # args = '%' + hotelCity + '%'

    # cur.execute("SELECT * FROM hotels WHERE hotel_city LIKE %s AND cluster = %s;", (args, int(res[0])))
    # hotel = cur.fetchall()

    result = int(res)

    # if len(hotel) != 0:
    #     result = insertMultipleData(hotel, cur)

    # cur.close()
    return responseSuccessJSON(200, "success get all hotel", result)

def insertMultipleData(items, cur):
    datas = []

    for item in items:
        cur.execute("SELECT hfacilities.hfacilities_id, hfacilities.facilities_name FROM tourisms JOIN hfacilities ON hfacilities.hotel_id = %s", (item[0],))
        fetchedFacilties = cur.fetchall()

        facilities = []

        if len(fetchedFacilties) == 0:
            facilities = []
        else:
            for facil in fetchedFacilties:
                facilities.append({
                    "id" : facil[0],
                    "name" : facil[2],
                    "image" : facil[3]
                })


        datas.append({
            "id" : item[0],
            "image" : item[1],
            "name" : item[2],
            "property_type" : item[3],
            "city" : item[4],
            "province_id" : item[5],
            "province_name" : item[6],
            "address" : item[7],
            "rating" : item[8],
            "min_price" : item[9],
            "max_price" : item[10],
            "facilities" : facilities,
            "latitude" : item[11],
            "longitude" : item[12],
            "cluster" : item[13],
            "created_at" : item[14],
            "updated_at" : item[15]
        })
    
    return datas

def recommend(score, hotelRating):
    normalizedHotelRate = (hotelRating - MIN_HOTEL_RATE) / (MAX_HOTEL_RATE - MIN_HOTEL_RATE)
    normalizedFacilRate = (score - MIN_FACIL_RATE) / (MAX_FACIL_RATE - MIN_FACIL_RATE)

    print("facil : ", normalizedFacilRate)
    print("hotel : ", normalizedHotelRate)

    new_param = [[normalizedHotelRate, normalizedFacilRate]]
    new_param = np.array(new_param)

    print(type(scaler))
    # scaler = MinMaxScaler()
    param_scaled = scaler.transform(new_param)

    result = kmeans.predict(param_scaled)
    print(result)

    return result

def calculateRate(facilities):
    base_dir = "D:/College/final-project/api_ta/controllers/recommendation/facilities.json"

    with open(base_dir) as file:
        datas = json.load(file)

    rate_score = 0
    for facility in facilities:
        i = 0
        while i < len(datas['facilities']):
            if facility == datas['facilities'][i]['name']:
                rate_score += datas['facilities'][i]['rating']
            i += 1
    
    return rate_score