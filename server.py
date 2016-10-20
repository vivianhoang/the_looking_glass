# import json
import os

# from jinja2 import StrictUndefined
from flask import Flask    #, render_template, request, flash, redirect, session, jsonify
# from flask_debugtoolbar import DebugToolbarExtension


# from model import connect_to_db, db, User, Category, UserCategory, 

app = Flask(__name__)
app.secret_key = "ABC"

# app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """ home page"""

    return "Welcome to Looking Glass"

  
    # return render_template('homepage.html')



# @app.route('/register_form')
# def get_form_to_fill_in():
#     """display the registration form to fill in"""


#     return render_template("register_form.html")


# @app.route('/register_form', methods=['POST'])
# def get_registration_info():
#     """Process registration"""


#     firstname = request.form.get("firstname")
#     lastname = request.form.get("lastname")
#     email = request.form.get("email")
#     password = request.form.get("password")
#     flash("Welcome %s %s. Please check the categories you're interested in." % (firstname,lastname))
#     #instantiate a user in the User database.
#     new_user = User.instantiate_user(firstname,lastname,email,password)
#     session['user_id'] = new_user.user_id 
    
#     return redirect('/declare_interests')

 
# @app.route("/declare_interests")
# def user_interests_form():
#     """ present a list of interests that the user can check. Displayes interests checked before"""
#     user_id = session['user_id']

#     category_names = categories.keys()
#     category_names.sort()
#     print category_names
#     category_list = get_declared_interests(user_id)


#     return render_template("declare_interests.html",
#                            category_names=category_names,
#                            category_list=category_list,
#                            )


# @app.route("/declare_interests" , methods=['POST'])
# def register_interests():
#     """"Get the user's interests and put them in the UserCategory Table"""
   
#     user_id = session['user_id']
#     if db.session.query(UserCategory):
#         db.session.query(UserCategory).filter_by(user_id=user_id).delete()
#         db.session.commit()

#     interests = request.form.getlist("interest_change")
#     interest_list = []
#     #look up the category id on every category(interest) chosen to put in the association table
#     for interest in interests:
# #         interest_add_on = db.session.query(Category.category_id).filter_by(category_name=interest).first()
# #         interest_list.append(interest_add_on[0])

# #     UserCategory.instantiate_usercategory(user_id,interest_list)
    
#     # return redirect("/")


# # @app.route("/login")
# # def login():
# #     """Log in Form"""



# #     return render_template("login.html")


# @app.route('/login',methods=['POST'])
# def login_process():
#     """ Process login."""


#     email = request.form.get('email')
#     password = request.form.get('password')
#     user = User.query.filter_by(email=email).first()

#     if not user:
#         flash ("Please Register First")
#         return render_template('homepage.html')
#     if user.password != password:
#         flash('Incorrect Password. Please try again.')
#         return redirect('/login')

#     session['user_id'] = user.user_id
#     session['user_name'] = personalize_name(user.user_id)
#     flash('Logged in')
   
#     return redirect('/')

    

# @app.route('/logout')
# def logout():
#     """Log out."""


#     session.clear()

#     flash('Logged out. Please log in to see your news')
  
#     return redirect('/')


if __name__ == '__main__':
    # app.debug = True
    # app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    # connect_to_db(app, os.environ.get("DATABASE_URL")) 
    # DebugToolbarExtension(app)
    app.run(host="0.0.0.0", port=5000)




