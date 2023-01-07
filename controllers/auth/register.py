from flask import Blueprint, jsonify, request
from flask_cors import CORS
from helpers import *
from passlib.hash import sha256_crypt

register = Blueprint('register', __name__)
cors = CORS(register, resources={r"/v1/*": {"origins": "*"}})

@register.route("/v1/register", methods = ['POST'])
def registerUser():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    province = request.form.get('province')
    city = request.form.get('city')

    res = isEmailTaken(email)

    if res:
        return responseFailJSON(400, "account already existed")
    else:
        conn = initializeDB()
        cur = conn.cursor()

        hashedPass = sha256_crypt.hash(password)

        cur.execute("INSERT INTO users VALUES (default, %s, %s, %s, %s, %s);", (name, email, hashedPass, province, city))
        conn.commit()

        cur.execute("SELECT * FROM users WHERE email = %s;", (email,))
        res = cur.fetchone()

        cur.close()

        data = {
            "id" : res[0],
            "name" : res[1],
            "email" : res[2],
            "password" : res[3],
            "province" : res[4],
            "city" : res[5]
        }

        return responseSuccessJSON(201, "success register user", data)

def isEmailTaken(email):
    conn = initializeDB()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email = %s;", (email,))
    user_detail = cur.fetchall()

    cur.close()

    for item in user_detail:
        if item[2] == email:
            return True

    return False


