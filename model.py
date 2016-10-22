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
    gender = db.Column(db.String(1000), nullable=False)
    past_jobs = db.Column(db.String(2000), nullable=True)
    introduction = db.Column(db.String(2000), nullable=True)
    company_name = db.Column(db.String(50), nullable=True)
    category = db.Column(db.String(500), db.ForeignKey("categories.name"))
    city = db.Column(db.String(20), db.ForeignKey("cities.name"))
    is_matched = db.Column(db.Boolean, default=False)

    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<User id=%s first_name=%s last_name=%s email=%s password=%s gender=%s \
                past_jobs=%s introduction=%s company_name=%s category=%s city=%s \
                is_matched=%s> " % (self.id,
                                    self.first_name,
                                    self.last_name,
                                    self.email,
                                    self.password,
                                    self.gender,
                                    self.past_jobs,
                                    self.introduction,
                                    self.company_name,
                                    self.category,
                                    self.city,
                                    self.is_matched)


class Mentee(db.Model):
    """Users who are mentees."""

    __tablename__ = "mentees"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = db.realtionship("User", backref=db.backref("mentees"), order_by=id)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Mentee id=%s user_id=%s>" % (self.id,
                                              self.user_id)


class Mentor(db.Model):
    """Users who are mentors."""

    __tablename__ = "mentors"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = db.realtionship("User", backref=db.backref("mentors"), order_by=id)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Mentee id=%s user_id=%s" % (self.id,
                                             self.user_id)


class MatchR(db.Model):
    """Representing all mentee/mentor who are potentially matched or are already matched."""

    __tablename__ = "match_requests"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    mentee_id = db.Column(db.Integer, db.ForeignKey("mentees.id"))
    mentor_id = db.Column(db.Integer, db.ForeignKey("mentors.id"))  # grab mentor's id when they choose to help a mentee
    status = db.Column(db.String(10), default="Pending")

    mentee = db.relationship("Mentee", backref=db.backref("match_requests", order_by=id))

    mentor = db.realtionship("Mentor", backref=db.backref("match_requests", order_by=id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Match id=%s mentee_id=%s mentor_id=%s status=%s>" % (self.id,
                                                                      self.mentee_id,
                                                                      self.mentor_id.
                                                                      self.status)


class Category(db.Model):
    """Category type."""

    __tablename__ = "categories"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<Category id=%s name=%s" % (self.id,
                                            self.name)


class City(db.Model):
    """Cities."""

    __tablename__ = "cities"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), primary_key=True)

    # backref is a simple way to also declare a new property on the Company_R class.
    # You can then also use a_review.user.first_name (a_review is a pre-created
    # query) to get the person who made the review.

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<City id=%s name=%s>" % (self.id,
                                         self.name)

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
