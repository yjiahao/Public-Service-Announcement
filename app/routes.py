import os

from app import app
from flask import request, abort, render_template, url_for, redirect
from sklearn.metrics.pairwise import cosine_similarity

import json

import pandas as pd
import numpy as np

from dotenv import load_dotenv

from sentence_transformers import SentenceTransformer

from langchain_openai import ChatOpenAI

load_dotenv()

# load pretrained encoding model, takes a while to load
model = SentenceTransformer('all-MiniLM-L6-v2')

# load dataset: should contain the embeddings generated by the model on the job description
jobs = pd.read_csv("data/preprocessed.csv")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html")

    elif request.method == "POST":
        # User's input: should get from form here using request...
        interests = request.form.get("interests")
        skills = request.form.get("skills")
        certs = request.form.get("qualification")
        jobhist = request.form.get("exp")
        psa_courses = request.form.get("psatraining")
        job_preference = request.form.get("pref")

        # Combine inputs into one sentence
        sentence = f'''
        Interests: {interests},
        Skills: {skills},
        Certifications: {certs},
        Job History: {jobhist},
        PSA courses taken: {psa_courses},
        Job Preference: {job_preference}
        '''

        # Encode the sentence into an embedding vector
        embeddings = model.encode([sentence])  # Assuming this outputs a list or array
        embeddings = np.array(embeddings).reshape(1, -1)  # Reshape to (1, n_features)

        # Make a copy of the job data
        temp_df = jobs.copy()

        # Ensure job embeddings are numpy arrays and properly shaped
        temp_df['embeddings'] = temp_df['embeddings'].apply(lambda x: np.array(json.loads(x)).reshape(1, -1))

        # Compute cosine similarity
        temp_df['similarity_score'] = temp_df['embeddings'].apply(lambda x: cosine_similarity(x, embeddings)[0][0])

        # Sort by similarity score in descending order
        temp_df = temp_df.sort_values(by='similarity_score', ascending=False)

        # Serve top 10 results
        top_10_jobs = temp_df.head(10)

        print(top_10_jobs)

        # reranker goes here
        recommendations = "Hello"
        return redirect(url_for("results", recommendations = recommendations))
    else:
        abort(400, description="Request method not supported")

@app.route("/results")
def results():
    recommendations = request.args.get("recommendations")
    return render_template("results.html", recommendations = recommendations)