import unittest
from forms import GrantForm  

class TestGrantForm(unittest.TestCase):

    def setUp(self):
        self.form = GrantForm()

    def test_get_next_question(self):
        # Test with a valid question number (e.g., num = 1)
        num = 1
        response = GrantForm.get_next_question(self.form, num)
        self.assertIsInstance(response, dict)
        self.assertIn("question", response)
        self.assertIn("form", response)
        self.assertTrue(response["question"])
        self.assertTrue(response["form"])

        # Test with an invalid question number (e.g., num = 0)
        num = 0
        response = GrantForm.get_next_question(self.form, num)
        self.assertIsNone(response)

        # Test with an out-of-range question number (e.g., num = 12)
        num = 12
        response = GrantForm.get_next_question(self.form, num)
        self.assertIsNone(response)
