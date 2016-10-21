"""Models and database functions for The Looking Glass."""

from flask_sqlalchemy import SQLAlchemy

# Connecting to the PostgreSQL database through the FLASK-SQLAlchemy helper library

db = SQLAlchemy()


# db.Model is the baseclass for all models.
class User(db.Model):
    """User information."""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    gender = db.Column(db.String(1000), nullable=True)  # can decide whether or not we want a gender
    past_jobs = db.Column(db.String(2000), nullable=True)
    introduction = db.Column(db.string(2000), nullable=True)
    interests = db.Column(db.String(500), nullable=True)
    mentor = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<User id=%s first_name=%s last_name=%s email=%s password=%s gender=%s \
                past_jobs=%s introduction=%s interests=%s mentor=%s> " % (self.id,
                                                                          self.first_name,
                                                                          self.last_name,
                                                                          self.email,
                                                                          self.password,
                                                                          self.gender,
                                                                          self.past_jobs,
                                                                          self.introduction,
                                                                          self.interests,
                                                                          self.mentor)


class Salary_R(db.Model):
    """Salary reviews."""

    __tablename__ = "salary_reviews"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    salary_review = db.Column(db.String(2500), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    date_time = db.Column(db.DateTime, nullable=False)

    user = db.relationship("Users", backref=db.backref("salary_review", order_by=id))

    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<Salary_R id=%s salary_review=%s user_id=%s> date_time=%s" % (self.id,
                                                                              self.salary_review,
                                                                              self.user_id,
                                                                              self.date_time)


class Company_R(db.Model):
    """Company reviews."""

    __tablename__ = "company_reviews"

    id = db.Column(db.Integer, autoincrement=True,
                   primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    company_name = db.Column(db.String(64), db.ForeignKey("company_names.name"))
    company_review = db.Column(db.String(2500), nullable=True)
    date_time = db.Column(db.DateTime, nullable=False)

    user = db.relationship("User", backref=db.backref("company_reviews", order_by=id))

    company = db.relationship("Company_N", backref=db.backref("company_reviews", order_by=id))

    # backref is a simple way to also declare a new property on the Company_R class. 
    # You can then also use a_review.user.first_name (a_review is a pre-created
    # query) to get the person who made the review.

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Company_R id=%s user_id=%s company_name=%s company_review=%s date_time=%s>" % (self.id,
                                                                                                self.user_id,
                                                                                                self.company_name,
                                                                                                self.company_review,
                                                                                                self.date_time)


class Company_N(db.Model):
    """Company names."""

    __tablename__ = "company_names"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(70), primary_key=True)
    address = db.Column(db.String(100), unique=False, nullable=False)  # do we want to make this nullable?

    company = db.relationship("Company_R", backref=db.backref("company_names", order_by=id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Company_N id=%s company_name %s address=%s is_owner=%s>" % (self.id,
                                                                             self.name,
                                                                             self.address)


class Mentee(db.Model):
    """Users who want to be mentees and need a mentor."""

    __tablename__ = "mentees"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    is_matched = db.Column(db.Boolean, default=False)
    help_description = db.Column(db.String(500), nullable=True)
    topic_id = db.Column(db.Integer, db.ForeignKey("topics.topic"))

    user = db.realtionship("User", backref=db.backref("mentees"), order_by=id)

    topic = db.relationship("Topic", backref=db.backref("mentees", order_by=id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Mentee id=%s user_id %s is_matched=%s help_description=%s> topic_id" % (self.id,
                                                                                         self.user_id,
                                                                                         self.is_matched,
                                                                                         self.help_description,
                                                                                         self.topic_id)


class Topic(db.Model):
    """Topics of what mentees need help on."""

    __tablename__ = "topics"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    topic = db.Column(db.String(64), primary_key=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Topic id=%s topic=%s>" % (self.id,
                                           self.topic)


class Match(db.Model):
    """When mentor selects to help a mentee."""

    __tablename__ = "matches"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    mentee_id = db.Column(db.Integer, db.ForeignKey("mentees.id"))
    mentor_id = db.Column(db.Integer, db.ForeignKey("users.id"))  # grab mentor's id when they choose to help a mentee

    mentee = db.relationship("Mentee", backref=db.backref("Match", order_by=id))

    user = db.realtionship("User", backref=db.backref("Match", order_by=id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Match id=%s mentee_id=%s mentor_id=%s>" % (self.id,
                                                            self.mentee_id,
                                                            self.mentor_id)

################################################################################

# Currently have the psql database as 'tlg'. Can change later.


def connect_to_db(app, db_uri='postgresql:///tlg'):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."
