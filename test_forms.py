import unittest
from forms import GrantForm  
import json

class TestGrantForm(unittest.TestCase):

    def setUp(self):
        self.form = GrantForm()

    def test_get_next_question(self):
        # Test with a valid question number (e.g., num = 1)
        num = 1
        response = GrantForm.get_next_question(self.form, num)
        self.assertTrue(isinstance(response, str))

        try:
            json_response = json.loads(response)
            self.assertIsInstance(json_response, dict)
            self.assertIn("question", json_response)
            self.assertIn("form", json_response)
            self.assertTrue(json_response["question"])
            self.assertTrue(json_response["form"])
        except json.JSONDecodeError:
            self.fail("Response is not valid JSON.")


        # Test with an invalid question number (e.g., num = 0)
        num = 0
        response = GrantForm.get_next_question(self.form, num)
        self.assertIsNone(response)

        # Test with an out-of-range question number (e.g., num = 12)
        num = 12
        response = GrantForm.get_next_question(self.form, num)
        self.assertIsNone(response)
