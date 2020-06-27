from flask import Flask
#from flask_cors import  CORS, cross_origin
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from Config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy()
db.init_app(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

from application.controllers import AuthController


@app.before_first_request
def create_tables():
    db.create_all()
