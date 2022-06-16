import os
import sqlite3

from flask import Flask, render_template, request

# function for retrieving twitter metadata
import tweetmetadata as tweet

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# From CS50 Finance
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Return apology message
def apology(message):
    """Render message as an apology to user."""
    
    return render_template("apology.html", message=message)

@app.route("/", methods=["GET", "POST"])
def index(): 

    if request.method == "POST":
        # Must enter input into form
        link = request.form.get("link")
        
        if not request.form.get("link"):
            return apology("Must enter link.")

        data = tweet.get_metadata(link)
        
        # Display graphic
        return render_template("new.html", data=data)
    
    if request.method == "GET":  
        return render_template("index.html")


# https://www.youtube.com/watch?v=CUIK3tKNH5E&ab_channel=CS50 