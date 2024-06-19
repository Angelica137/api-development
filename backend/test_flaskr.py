import os
import psycopg2
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

        self.app = create_app({"SQLALCHEMY_DATABASE_URI": self.database_path})
        self.client = self.app.test_client

        # Push an application context
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.db = SQLAlchemy()
        self.db.init_app(self.app)
        self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        self.db.session.remove()
        self.db.drop_all()
        self.app_context.pop()

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

    def test_search_questions(self):
        question1 = Question(
            question='What is the capital of France?',
            answer='Paris',
            difficulty=2,
            category=3)
        question2 = Question(
            question='What is the largest planet in our solar system?',
            answer='Jupiter',
            difficulty=3,
            category=2)
        question3 = Question(
            question='Who painted the Mona Lisa?',
            answer='Leonardo da Vinci',
            difficulty=2,
            category=2)

        self.db.session.add_all([question1, question2, question3])
        self.db.session.commit()

        search_term = {'searchTerm': 'France'}
        res = self.client().post('/questions/search', json=search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['questions'], list)
        self.assertGreater(len(data['questions']), 0)
        self.assertIsInstance(data['total_questions'], int)
        self.assertGreater(data['total_questions'], 0)

        search_term = {'searchTerm': 'Nonexistent'}
        res = self.client().post('/questions/search', json=search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['questions'], list)
        self.assertEqual(len(data['questions']), 0)
        self.assertIsInstance(data['total_questions'], int)
        self.assertEqual(data['total_questions'], 0)

        search_term = {'searchTerm': ''}
        res = self.client().post('/questions/search', json=search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['questions'], list)
        self.assertGreater(len(data['questions']), 0)
        self.assertIsInstance(data['total_questions'], int)
        self.assertGreater(data['total_questions'], 0)

    def test_get_questions_by_category(self):
        category1 = Category(type='Science')
        category2 = Category(type='History')
        self.db.session.add_all([category1, category2])
        self.db.session.commit()

        question1 = Question(
            question='What is the capital of France?',
            answer='Paris',
            category=category1.id,
            difficulty=2)
        question2 = Question(
            question='Who painted the Mona Lisa?',
            answer='Leonardo da Vinci',
            category=category2.id,
            difficulty=3)
        self.db.session.add_all([question1, question2])
        self.db.session.commit()

        res = self.client().get(f'/categories/{category1.id}/questions')
        print(f"Response data: {res.data}")  # Print the res data
        print(f"Status code: {res.status_code}")  # Print the status code
        # Parse response data as text
        data = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['questions'], list)
        self.assertEqual(len(data['questions']), 1)
        self.assertEqual(data['total_questions'], 1)
        self.assertEqual(data['current_category'], category1.type)

        res = self.client().get('/categories/999/questions')
        # Parse response data as text
        data = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not Found')

    def test_404_error(self):
        # Test case 1: Request a non-existent resource
        res = self.client().get('/non-existent-resource')
        data = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not Found')



if __name__ == "__main__":
    unittest.main()
