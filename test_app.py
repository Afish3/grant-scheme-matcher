import unittest
from flask import Flask, session

from app import app

class YourAppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        # Clean up after each test if needed
        pass

    def test_index_route_with_session_data(self):
        with self.app as client:
            with client.session_transaction() as sess:
                # Set session data for testing, e.g., eligible grants
                sess['eligible_grants'] = [1, 2, 3]
                sess['responses'] = {'question1': 'answer1', 'question2': 'answer2'}
            
            # Make a GET request to the index route
            response = client.get('/')
            
            # Assertions to check if the response contains expected content
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Your HTML content here', response.data)

    def test_index_route_without_session_data(self):
        with self.app as client:
            # Make a GET request to the index route without setting session data
            response = client.get('/')
            
            # Assertions to check if the response contains expected content
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Your HTML content here', response.data)
