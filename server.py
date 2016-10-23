# import json
import os

from jinja2 import StrictUndefined
from flask import (Flask, render_template, request, flash, redirect, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension


from model import connect_to_db, db, User, Mentee, Mentor, MatchR, Category, City
import dictalchemy

app = Flask(__name__)
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


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

    user = User.query.filter(User.email == email).first()

    # Check to see if they are already registered user.
    # If in database, redirect them to index with flash message "You are already registered. Please log in"
    if email == user:
        flash("You are already a registered user. Please login.")
        return redirect('/')
    # Else if they a new user, Add to user table
    else:
        user = User(first_name=firstname,
                    last_name=lastname,
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
                    )
        db.session.add(user)
        db.session.commit()
        flash("You have been added.")
        session['id'] = user.id

        # Check to see if user is a mentee or mentor
        # have to put the user into right database
        if role == "mentor":
            mentor = Mentor(user_id=session['id'],
                )
            db.session.add(mentor)
            db.session.commit()
            return redirect('/search.html')
        else:
            mentee = Mentee(user_id=session['id'],
                )
            db.session.add(mentee)
            db.session.commit()
            return redirect('profile.html')


@app.route('/login', methods=["POST"])
def login():
    """Login page for existing user."""

    email = request.form.get('email')
    password = request.form.get('password')
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


@app.route('/mentor', methods=['GET'])
def mentor():
    """Landing page for mentor login."""

    # Page with pending mentee matches

    return render_template("mentor.html")


# This route will display the member's profile
@app.route('/profile/<id>')
def display_profile(id):

    # Page with user profile including first name, last name, email, etc

    user = User.query.filter(User.id == id).one()
    # mentee = Mentee.query.filter(Mentee.user_id == id).one()
    mentor = Mentor.query.filter(Mentor.user_id == id).one()
    categories = Category.query.all()
    cities = City.query.all()

    # if mentee:
        # return render_template("profile.html", user=user, mentee=mentee)

    if mentor:
        return render_template("profile.html", user=user, mentor=mentor, categories=categories, cities=cities)

    return render_template("profile.html", user=user, cities=cities)
    # first_name = user.first_name
    # last_name = user.last_name
    # email = user.email
    # gender = user.gender
    # past_jobs = user.past_jobs
    # phone = user.phone
    # introduction = user.introduction
    # company_name = user.company_name
    # category_id = user.category_id
    # city_id = user.city_id
    # url = user.url

    # return render_template("profile.html", user=user)
                            # first_name=first_name,
                            # last_name=last_name,
                            # email=email,
                            # gender=gender,
                            # past_jobs=past_jobs,
                            # phone=phone,
                            # introduction=introduction,
                            # company_name=company_name,
                            # category_id=category_id,
                            # city_id=city_id,
                            # url=url)


@app.route('/profile-edit', methods=['POST'])
def update_profile():
    """Editing profile."""

    category_id = request.form.get("category")
    company = request.form.get("company-name")
    description = request.form.get("description")
    past_jobs = request.form.get("prev-experience")
    city = request.form.get("city")
    url = request.form.get("url")

    data = {"category_id": category_id,
            "company_name": company,
            "introduction": description,
            "past_jobs": past_jobs,
            "city_name": city,
            "url": url}

    User.query.filter_by(user_id=session['id']).update(data)

    db.session.commit()

    return "You have successfully updated your profile."


@app.route('/find-mentors')
def available_mentors():
    """Display all available mentors."""

    #mentors = Mentor.query.filter(Mentor.user.company_name != "--").all()
    mentors = Mentor.query.all()
    categories = Category.query.all()
    cities = City.query.all()

    return render_template("search.html", categories=categories, cities=cities, mentors=mentors)
# find available mentors
# if user is a mentor AND they have chosen a category they want to mentor in,
# render template and display all the mentors

@app.route('/mentors.json')
def get_mentors():
    """Return list of mentors in json."""

    search_results = Mentor.query.all()
    mentors_dict = {}

    for counter, result in enumerate(search_results, 1):
        # print result.user.first_name, result.user.city_id

        if result.user.city_id == 17:
            mentor = dictalchemy.utils.asdict(result.user)
            mentor['mentor_id'] = result.id
            mentors_dict['mentor' + str(counter)] = mentor

    # print mentors_dict

    return jsonify(mentors_dict)



@app.route('/match-pending', methods=["POST"])
def match_pending():
    """Mentee selects interest in a mentor."""

    mentor_id = request.form.get("mentor_id")
    # not sure if querying for mentee id is correct
    mentee_id = Mentee.query.filter_by(Mentee.user.user_id == session['id']).one()
    # user = User.query.filter_by(user_id=session['id']).first()

    new_pending = MatchR(mentee_id=mentee_id, mentor_id=mentor_id)

    db.session.add(new_pending)
    db.session.commit()

    return render_template("/SOME CONFIRMATION PAGE")


@app.route('/match', methods=["POST"])
def match():
    """Mentor accepts a mentee's request for mentorship."""

    # need to find out how to find mentee id and mentor id

    # MatchR.query.filter(mentee_id=mentee_id, mentor_id=mentor_id).update({"status": "Matched"})

    # db.session.commit()

    return redirect('/SOMEWHERE-LOL. Probably to a chatting page.')


@app.route('/logout')
def logout():
    """User log out."""

    flash("You have successfully logged out.")
    return redirect('/')



if __name__ == '__main__':
    app.debug = True
    # app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0", port=5000)




