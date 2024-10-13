from app import app
from flask import request, abort, render_template, url_for

# test route for home
@app.route("/", methods = ["GET", "POST"])
def home():
    # if user is accessing the page directly
    if request.method == "GET":
        # return render_template("index.html"): supposed to render the html template here
        return render_template("index.html")
    # elif user submits the form on the page
    elif request.method == "POST":
        # create vector embeddings of the sentences user types in, then perform vector search here as well
        # arrange the rows and return top k relevant results
        return "Under development"
    else:
        # otherwise, if request is not GET/POST
        abort(400, description="Request method not supported")