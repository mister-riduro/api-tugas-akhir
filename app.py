from flask import Flask
from register import register
from login import login

app = Flask(__name__)

app.register_blueprint(register)
app.register_blueprint(login)

if __name__ == "__app__":
    app.run()