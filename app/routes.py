from app import app
from flask import request, abort

# test route for home
@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "GET":
        return "Hello world!"
    elif request.method == "POST":
        return "Under development"