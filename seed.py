"""Utility file to seed food databse from Yelp's available categories"""

from model import Category, City, connect_to_db, db
from server import app


def load_cities():
    """Load cities into database."""

    cities = []

    for row in (open('cities.txt')):
        city = row.rstrip()
        cities.append(city)

    ordered_cities = sorted(cities)

    for city in ordered_cities:
        find_city = City.query.filter_by(name=city).first()
        if not find_city:
            city = City(name=city)
            db.session.add(city)

    db.session.commit()
    print "Cities loaded."


def load_job_categories():
    """Load job categories into database."""

    jobs = []

    for row in (open('job-categories.txt')):
        job = row.rstrip()
        jobs.append(job)

    sorted_jobs = sorted(jobs)

    for job in sorted_jobs:
        find_job = Category.query.filter_by(name=job).first()
        if not find_job:
            job = Category(name=job)
            db.session.add(job)

    db.session.commit()
    print "Job cateogires loaded"


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

load_cities()
load_job_categories()
