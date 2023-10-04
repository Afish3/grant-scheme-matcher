"""Models for Grant Matcher."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect this database to provided Flask app.

    call this in Flask app.
    """

    db.app = app
    db.init_app(app)


class User(db.Model):
    """Site user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_responses = db.Column(db.JSON, nullable=True)
    date_accessed = db.Column(db.DateTime, nullable=False, default=datetime.now)

    grants = db.relationship("Grants", secondary="user_grants", backref="users", cascade="all,delete")

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

class UserGrants(db.Model):
    """Grants for users."""

    __tablename__ = "user_grants"

    grant_id = db.Column(db.Integer, db.ForeignKey('grants.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

class Grants(db.Model):
    """Grants."""

    __tablename__ = "grants"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)

    @classmethod
    def calculate_amount(cls, grant_num, size, age, amount_of_applicants):
        if grant_num == 1:
            min_amount = 0
            if size == 'Less than 0.25 hectares':
                max_amount = 1200
            elif size == 'Less than 3 hectares':
                max_amount = 12000
            elif size == 'Between 3 and 5 hectares':
                max_amount = 24000
            elif size == 'Between 3 and 10 hectares':
                max_amount = 69000
            elif size == 'Between 3 and 100 hectares':
                max_amount = 418000
            return [min_amount, max_amount]
        elif grant_num == 2:
            min_amount = 0
            if size == 'Less than 0.25 hectares' or size == 'Less than 3 hectares' or size == 'Between 3 and 5 hectares' or size == 'Between 3 and 10 hectares':
                max_amount = 2500
            elif size == 'Between 3 and 100 hectares':
                max_amount = 10000
            return [min_amount, max_amount]
        elif grant_num == 3:
            min_amount = 0
            if size == 'Between 3 and 5 hectares':
                max_amount = 17500
            else:
                max_amount = '~'
            return [min_amount, max_amount]
        elif grant_num == 4:
            min_amount = 0
            if age == 'Yes, all owners are under the age of 41':
                max_amount = '%60 - %90'
            else:
                max_amount = '%40 - %80'
            return [min_amount, max_amount]
        elif grant_num == 5:
            min_amount = 0
            if amount_of_applicants == 'The land is individually owned':
                max_amount = 25000
            else:
                max_amount = 125000
            return [min_amount, max_amount]
        elif grant_num == 6:
            min_amount = 0
            max_amount = 1000
            return [min_amount, max_amount]
        return 0
    
def track_new_form_submission(grants, responses):
    user = User(user_responses = responses)
    grants_to_add = [Grants.query.get(grant_id) for grant_id in grants]
    user.grants.extend(grants_to_add)
    db.session.add(user)
    db.session.commit()