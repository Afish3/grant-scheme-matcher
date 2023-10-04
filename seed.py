"""Seed file to add grants to the database."""

from model import Grants, db
from app import app, grant_titles

def seed_database():
    with app.app_context():

        # Create all tables
        db.drop_all()
        db.create_all()

        # If table isn't empty, empty it
        Grants.query.delete()

        i = 0
        for title in grant_titles:
            i += 1
            grant = Grants(id=i, name=title)
            db.session.add(grant)
        
        db.session.commit()

seed_database()