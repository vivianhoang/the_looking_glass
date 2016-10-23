# import json
import os

# from jinja2 import StrictUndefined
from flask import (Flask, render_template, request, redirect, session, jsonify)
# from flask_debugtoolbar import DebugToolbarExtension


from model import connect_to_db, db, User, Mentee, Mentor, MatchR, Category, City

app = Flask(__name__)
app.secret_key = "ABC"

# app.jinja_env.undefined = StrictUndefined


@app.route('/', methods=["GET","POST"])
def homepage():
    """Register page"""


    return render_template("index.html")


#first welcome page after user signs up
#form.get. value whether or not they are a mentee or mentor




# This route will display the member's profile
@app.route('/profile/<id>')
def display_profile():

    return render_template("profile.html")


@app.route('/logout')
def logout():
    """User log out."""

    return redirect('/')




if __name__ == '__main__':
    # app.debug = True
    # app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    connect_to_db(app) 
    # DebugToolbarExtension(app)
    app.run(host="0.0.0.0", port=5000)




