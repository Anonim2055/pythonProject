from flask import Flask
from pymongo import MongoClient
from flask_jwt_extended import JWTManager



app = Flask(__name__)

try:
    mongo = MongoClient(host="localhost",port=27018,serverSelectionTimeoutMS=5000)
    db = mongo.flask

    print("MongoDB Connect")
except Exception:
    print("Unable to connect MongoDB")




# change this!
app.secret_key = 'your-secret-key'

from .routes.users import users
from .routes.index import main

app.register_blueprint(main)
app.register_blueprint(users)



