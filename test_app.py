import unittest
from flask import Flask, session, url_for

from app import app

class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_index_route_with_session_data(self):
        with self.app as client:
            with client.session_transaction() as sess:
                # Set session data for testing, e.g., eligible grants
                sess['eligible_grants'] = [1, 2, 3]
                sess['responses'] = {'question1': 'answer1', 'question2': 'answer2', 'question3': 'answer3', 'question4': 'answer4', 'question5': 'answer5', 'question6': 'answer6', 'question7': 'answer7', 'question8': 'answer8', 'question9': 'answer9', 'question10': 'answer10', 'question11': 'answer11'}
            
            # Make a GET request to the index route
            response = client.get('/')
            
            # Assertions to check if the response contains expected content
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Your Responses', response.data)

    def test_index_route_without_session_data(self):
        with self.app as client:
            # Make a GET request to the index route without setting session data
            response = client.get('/')
            
            # Assertions to check if the response contains expected content
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Find grants to fund your environmental project!', response.data)

    def test_show_question_redirect(self):
        with self.app as client:
            with client.session_transaction() as sess:
                # Simulate a session with responses for testing
                sess['responses'] = {1: 'Yes', 2: 'No'}  

            # Replace this with the appropriate URL for your route
            response = client.get('/form/question/3')

            # Assert that the response status code is a redirect (302)
            self.assertEqual(response.status_code, 302)

            # Assert that the response redirects to the correct URL
            self.assertRedirects(response, url_for('show_question', num=4))

    def test_post_response(self):
        with self.app as client:
            with client.session_transaction() as sess:
                # Simulate a session with responses for testing
                sess['responses'] = {1: 'Yes', 2: 'No'}  

            # Replace this with the appropriate URL for your route
            response = client.post('/post/response/3', data={'q3': 'Some answer'})

            # Assert that the response status code is a redirect (302)
            self.assertEqual(response.status_code, 302)

            # Assert that the response redirects to the correct URL
            self.assertRedirects(response, url_for('show_question', num=4))

            # Assert that the session has been updated with the new response
            self.assertEqual(session['responses']['If this land is currently being used, what is it being used for?'], 'Some answer')

    def test_go_to_previous_question(self):
        with self.client:
            # Simulate an existing session with a response
            with self.client.session_transaction() as sess:
                sess['responses'] = {'Question 1': 'Answer 1'}

            # Make a GET request to /back
            response = self.client.get('/back')

            # Assert that the response status code is a redirect (HTTP 302)
            self.assertEqual(response.status_code, 302)

            # Assert that the session was updated correctly (the last question was removed)
            with self.client.session_transaction() as sess:
                responses = sess.get('responses', {})
                self.assertNotIn('Question 1', responses)  # Ensure 'Question 1' is removed

            # Assert that the response redirects to the previous question
            self.assertRedirects(response, '/form/question/1') 