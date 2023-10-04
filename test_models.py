import unittest
from model import Grants

class TestModels(unittest.TestCase):

    def test_calculate_amount(self):
        """Test that calculate_amount returns a list of values"""

        grant_num = 1
        size = 'Less than 0.25 hectares'
        age = 'Yes, all owners are under the age of 41'
        amount_of_applicants = 'The land is individually owned'

        result = Grants.calculate_amount(grant_num, size, age, amount_of_applicants)

        # Assert the result is a list
        self.assertIsInstance(result, list)

        # Assert that the result is not empty
        self.assertTrue(result)