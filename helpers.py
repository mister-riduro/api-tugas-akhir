from flask import jsonify, request
from functools import wraps
from dotenv import load_dotenv

import jwt
import os
import psycopg2
import datetime
import jwt

import cloudinary
import cloudinary.uploader
import cloudinary.api

def initializeENV():
    load_dotenv()

def initializeDB():
    initializeENV()

    conn = psycopg2.connect(
            host="localhost",
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USERNAME'),
            password=os.getenv('DB_PASSWORD'))
    return conn

def uploadImage(image):
    initializeENV()
    cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))

    
    uploadImageResult = cloudinary.uploader.upload(image)
    imageURL = uploadImageResult['url']

    return imageURL