# import json
import os

# from jinja2 import StrictUndefined
from flask import (Flask, render_template, request, redirect, session, jsonify)
# from flask_debugtoolbar import DebugToolbarExtension


from model import connect_to_db, db, User, Mentee, Mentor, MatchR, Category, City

app = Flask(__name__)
app.secret_key = "ABC"

# app.jinja_env.undefined = StrictUndefined


@app.route('/', methods=["GET"])
def homepage():
    """Register page."""

    return render_template("index.html")

@app.route('/register', methods=["POST"])
def register():
    """If user registers."""

    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    email = request.form.get("email")
    password = request.form.get("password")
    gender = request.form.get("gender")
    # past_jobs = request.form.get("past_jobs")
    # phone = request.form.get("phone")
    # introduction = request.form.get("introduction")
    # company_name = request.form.get("company_name")
    # category_id = request.form.get("category_id")
    # city_id = request.form.get("city_id")
    # url = request.form.get("url")
    role = request.form.get("role")

    user = User.query.filter(User.email == email).first())
    
    # Check to see if they are already registered user.
    # If in database, redirect them to index with flash message "You are already registered. Please log in"
    if email == user:
        flash("You are already a registered user. Please login.")
        return redirect('/')
    # Else if they a new user, Add to user table
    else: 
        user = User(firstname=firstname, 
                    lastname=lastname,
                    email=email, 
                    password=password,
                    gender=gender,
                    # past_jobs=past_jobs,
                    # phone=phone,
                    # introduction=introduction,
                    # company_name=company_name,
                    # category_id=category_id,
                    # city_id=city_id,
                    # url=url,
                    role=role
                    ) 
        db.session.add(user)
        db.session.commit()
        flash("You have been added.")
        session['id'] = user.id

        # Check to see if user is a mentee or mentor 
        # have to put the user into right database
        if role = "Mentor":
            mentor = Mentor(user_id=session['id'],
                )
            db.session.add(mentor)
            db.session.commit()
            print "works."
            return
            # return redirect('/search.html')
        else:
            mentee = Mentee(user_id=session['id'],
                )
            db.session.add(mentee)
            db.session.commit()
            print "works."
            return
            # return redirect('profile.html')


@app.route('/login', methods=["POST"])
def login():
    """Login page for existing user."""

    email = request.form.get('email')
    password =request.form.get('password')
    user = User.query.filter_by(email=email).first()

    if not user:
        flash("Please register first.")
        return redirect('/')
    if user.password != password:
        flash("Incorrect password. Please try again.")
        return redirect('/')

    session['id'] = user.id
    flash('Logged in')

    return redirect('/')


@app.route('/mentee', methods=['GET'])
def mentee():
    """Landing for existing mentee."""

    # Page with Matches and pending matches. 

    return render_template("mentee.html")


@app.route('/mentor', methods['GET'])
def mentor():
    """Landing page for mentor login."""

    # Page with pending mentee matches 

    return render_template("mentor.html")


# This route will display the member's profile
@app.route('/profile/<id>')
def display_profile():

    # Page with user profile including first name, last name, email, etc

    return render_template("profile.html")


@app.route('/logout')
def logout():
    """User log out."""

    flash("You have successfully logged out.")
    return redirect('/')



if __name__ == '__main__':
    # app.debug = True
    # app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    connect_to_db(app) 
    # DebugToolbarExtension(app)
    app.run(host="0.0.0.0", port=5000)




