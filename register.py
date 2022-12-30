from flask import Blueprint, jsonify, request
from flask_cors import CORS
import os

import psycopg2
from dotenv import load_dotenv
from passlib.hash import sha256_crypt

load_dotenv()

register = Blueprint('register', __name__)
cors = CORS(register, resources={r"/v1/*": {"origins": "*"}})

def init_db():
    conn = psycopg2.connect(
        host="localhost",
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD'))
    
    return conn

@register.route("/v1/register", methods = ['POST'])
def register_user():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    province = request.form.get('province')
    city = request.form.get('city')

    res = isEmailTaken(email)

    if res:
        return_json = {
            "status" : 400,
            "message" : "account already exist",
        }

        return jsonify(return_json)
    else:
        conn = init_db()
        cur = conn.cursor()

        hashedPass = sha256_crypt.hash(password)

        cur.execute("INSERT INTO users VALUES (default, %s, %s, %s, %s, %s);", (name, email, hashedPass, province, city))
        conn.commit()

        cur.execute("SELECT * FROM users WHERE email = %s;", (email,))
        res = cur.fetchone()

        cur.close()

        return_json = {
            "status" : 201,
            "message" : "user registered",
            "data" : {
                "id" : res[0],
                "name" : name,
                "email" : email,
                "password" : hashedPass,
                "province" : province,
                "city" : city
            }
        }

        return jsonify(return_json)

def isEmailTaken(email):
    conn = init_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email = %s;", (email,))
    user_detail = cur.fetchall()

    cur.close()

    for item in user_detail:
        if item[2] == email:
            return True

    return False


