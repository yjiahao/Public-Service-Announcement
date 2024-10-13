from app import app
from flask import request, abort

# test route for home
@app.route("/", methods = ["GET"])
def home():
    return "Hello world!"