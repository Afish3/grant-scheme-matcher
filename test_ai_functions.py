import unittest
import os

from app import get_knowledge_base 

class TestAIFunctions(unittest.TestCase):

    def test_creates_all_grants_pkl_file(self):
        # Remove the all_grants.pkl file if it exists to start with a clean slate
        if os.path.exists('all_grants.pkl'):
            os.remove('all_grants.pkl')

        # Call the function
        knowledge_base = get_knowledge_base()

        # Check if the file exists
        self.assertTrue(os.path.exists('all_grants.pkl'))
