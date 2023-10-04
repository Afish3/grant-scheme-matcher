"""Models for Grant Matcher."""

from flask_sqlalchemy import SQLAlchemy

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

    grants = db.relationship("Grants", backref="user", cascade="all,delete")

class Grants(db.Model):
    """Grants."""

    __tablename__ = "grants"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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