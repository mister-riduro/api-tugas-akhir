from flask import Flask
from controllers.auth.register import register
from controllers.auth.login import login
from controllers.tourism.nearest_event import nearestEvent
from flask_jwt_extended import JWTManager
from helpers import initializeENV

import os

app = Flask(__name__)

initializeENV()
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

app.register_blueprint(register)
app.register_blueprint(login)
app.register_blueprint(nearestEvent)
JWTManager(app)

if __name__ == "__app__":
    app.run()