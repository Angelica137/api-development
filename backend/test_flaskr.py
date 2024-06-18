import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category, db

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)

        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })

        self.client = self.app.test_client

        # Bind the app to the current context to allow delete object
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['categories']), 6)
        self.assertIn('categories', data)
        self.assertIsInstance(data['categories'], dict)

    def test_get_questions(self):
        res = self.client().get('/questions?page=1')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']) <= 10)
        self.assertIn('questions', data)
        self.assertIsInstance(data['questions'], list)

        if len(data['questions']) > 0:
            question = data['questions'][0]
            self.assertIn('id', question)
            self.assertIn('question', question)
            self.assertIn('answer', question)
            self.assertIn('difficulty', question)
            self.assertIn('category', question)
            self.assertIsInstance(question['id'], int)
            self.assertIsInstance(question['question'], str)
            self.assertIsInstance(question['answer'], str)
            self.assertIsInstance(question['difficulty'], int)
            self.assertIsInstance(question['category'], int)

    def test_delete_question(self):
        question = Question(
            question='What is the capital of France?',
            answer='Paris',
            difficulty=1,
            category=1)
        db.session.add(question)
        db.session.commit()

        res = self.client().delete(f'/questions/{question.id}')
        print(res.get_json())  # Print response to debug
        print(res.data)
        print(res.headers)
        self.assertEqual(res.status_code, 200)

        res = self.client().get(f'/questions/{question.id}')
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
