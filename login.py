from flask import Blueprint, request, jsonify
from flask_cors import CORS
from passlib.hash import sha256_crypt
import os

import psycopg2
import jwt
import datetime
from dotenv import load_dotenv

load_dotenv()

login = Blueprint('login', __name__)
cors = CORS(login, resources={r"/v1/*": {"origins": "*"}})

def init_db():
    conn = psycopg2.connect(
        host="localhost",
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD'))
    
    return conn

@login.route("/v1/login", methods = ['POST'])
def login_user():
    email = request.form.get('email')
    password = request.form.get('password')

    conn = init_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email = %s;", (email,))
    res_db = cur.fetchone()
    cur.close()

    if len(res_db) == 0:
        return_json = {
            "status" : 404,
            "message" : "account doesn't exist",
        }

        return jsonify(return_json)
    
    res = sha256_crypt.verify(password, res_db[3])

    if res:
        token = jwt.encode({'user_id' : res_db[0], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, os.getenv('SECRET_KEY'), "HS256")

        return_json = {
            "status" : 200,
            "message" : "success login",
            "data" : {
                "token" : token
            }
        }

        return jsonify(return_json)
    else:
        return_json = {
            "status" : 400,
            "message" : "wrong email or password",
        }

        return jsonify(return_json)