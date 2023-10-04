import unittest
from app import app
from model import db, User, Grants, track_new_form_submission

app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///grants-test' 
app.config['SQLALCHEMY_ECHO'] = False

class TestFormSubmission(unittest.TestCase):

    def setUp(self):
        # Set up a test Flask app and database 
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""

        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_form_submission(self):
       with app.app_context():
            # Define sample data for testing
            sample_grants = [1, 2, 3]  # List of grant IDs
            sample_responses = {
                'question1': 'Answer1',
                'question2': 'Answer2',
                # Include more sample responses as needed
            }

            # Call the function with the sample data
            track_new_form_submission(sample_grants, sample_responses)

            # Check if a user was created with the responses and grants
            user = User.query.first()
            self.assertIsNotNone(user)
            self.assertEqual(user.user_responses, sample_responses)

            # Check if the user has the expected grants associated with them
            grants = user.grants
            self.assertEqual(len(grants), len(sample_grants))
            grant_ids = {grant.id for grant in grants}
            self.assertEqual(grant_ids, set(sample_grants))
