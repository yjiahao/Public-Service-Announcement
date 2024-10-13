from app import app
from flask import request, abort, render_template, url_for

import pandas as pd

from sentence_transformers import SentenceTransformer

# load pretrained encoding model, takes a while to load
# model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

# test route for home
@app.route("/", methods = ["GET", "POST"])
def home():
    # if user is accessing the page directly
    if request.method == "GET":
        # return render_template("index.html"): supposed to render the html template here with the forms and everything
        return render_template("index.html")
    # elif user submits the form on the page
    elif request.method == "POST":
        # create vector embeddings of the sentences user types in, then perform vector search here as well
        # arrange the rows and return top k relevant results
        
        # sentences = ["This is an example sentence"]
        # embeddings = model.encode(sentences)
        # return render_template("index.html", embeddings = embeddings)
        return "Under development"
    else:
        # otherwise, if request is not GET/POST
        abort(400, description="Request method not supported")