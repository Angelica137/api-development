import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)

        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })

        self.client = self.app.test_client

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for
    expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        # Check the success fuled in the the response data is True
        self.assertTrue(data['success'])
        self.assertTrue(len(data['categories']), 6)
        # check 'categories' key is in reponse obj
        self.assertIn('categories', data)
        # check categories is a dictionary
        self.assertIsInstance(data['categories'], dict)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
