from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = "secret key"
#Velocis Database is being used
app.config["MONGO_URI"] = "mongodb://localhost:27017/velocis"
mongo = PyMongo(app)
#print("Hello!") 
