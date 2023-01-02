from flask import Blueprint, request, jsonify
from flask_cors import CORS
from passlib.hash import sha256_crypt
from helpers import *
from flask_jwt_extended import create_access_token

login = Blueprint('login', __name__)
cors = CORS(login, resources={r"/v1/*": {"origins": "*"}})

initializeENV()

@login.route("/v1/login", methods = ['POST'])
def loginUser():
    email = request.form.get('email')
    password = request.form.get('password')

    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email = %s;", (email,))
    res_db = cur.fetchone()
    cur.close()

    if len(res_db) == 0:
        return_json = {
            "status" : 404,
            "message" : "account doesn't exist",
        }

        return return_json
    
    res = sha256_crypt.verify(password, res_db[3])

    if res:
        token = create_access_token(identity=res_db[0])

        return_json = {
            "status" : 200,
            "message" : "success login",
            "data" : {
                "token" : token
            }
        }

        return return_json
    else:
        return_json = {
            "status" : 400,
            "message" : "wrong email or password",
        }

        return return_json