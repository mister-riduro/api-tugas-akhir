from flask import Flask, jsonify, request
import psycopg2
from dotenv import load_dotenv

app = Flask(__name__)

def init_db():
    conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user=load_dotenv('DB_USERNAME'),
        password=load_dotenv('DB_PASSWORD'))
    
    return conn

@app.route("/v1/register", methods = ['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    province = request.form.get('province')
    city = request.form.get('city')

    res = check_user_email(email)

    if res:
        return_json = {
            "status" : 400,
            "message" : "account already exist",
        }

        return jsonify(return_json)
    else:
        conn = init_db()
        cur = conn.cursor()

        cur.execute(""" INSERT INTO users VALUES (%s, %s, %s, %s, %s)""", (name, email, password, province, city))
        conn.commit()

        return_json = {
            "status" : 201,
            "message" : "user registered",
        }

        return jsonify(return_json)



def check_user_email(email):
    conn = init_db()
    cur = conn.cursor()

    cur.execute(""" SELECT emails FROM users; """)
    user_email = cur.fetchall

    for item in user_email:
        if item == email:
            return False
    
    return True


