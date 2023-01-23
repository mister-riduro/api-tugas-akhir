from flask import Blueprint, request
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity

from helpers import *

from datetime import datetime

users = Blueprint('users', __name__)
cors = CORS(users, resources={r"/v1/*": {"origins": "*"}})

@users.route("/v1/users", methods = ['GET'])
@jwt_required()
def getDetailInformationUser():
    userID = get_jwt_identity()

    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE user_id = %s", (userID,))
    result = cur.fetchone()

    cur.close()

    data = {
        'name' : result[1],
        'email' : result[2],
        'province' : result[4],
        'city' : result[5]
    }

    return responseSuccessJSON(200, "success get user detail", data)

@users.route("/v1/users", methods = ['PUT'])
@jwt_required()
def updateDetailInformationUser():
    userName = request.form.get('name')
    userEmail = request.form.get('email')
    userProvince = request.form.get('province')
    userCity = request.form.get('city')

    userID = get_jwt_identity()

    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("UPDATE users SET name = %s, email = %s, province = %s, city = %s WHERE user_id = %s;", (userName, userEmail, userProvince, userCity ,userID,))
    conn.commit()

    cur.execute("SELECT * FROM users WHERE user_id = %s", (userID,))
    result = cur.fetchone()

    cur.close()

    data = {
        'name' : result[1],
        'email' : result[2],
        'province' : result[4],
        'city' : result[5]
    }

    cur.close()

    return responseSuccessJSON(200, "success update user detail", data)
