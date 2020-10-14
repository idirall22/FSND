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
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass
    
    def test_get_all_categories(self):
        response = self.client().get('/categories')
        self.assertEqual(response.status_code, 200)

    def test_get_questions(self):
        response = self.client().get('/questions?page=1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(data['questions']), 10)

    def test_delete_question(self):
        id = 1
        res = self.client().delete(f'/questions/{id}')
        data = json.loads(res.data)
        
        if res.status_code == 404:
            self.assertEqual(data['success'], False)
        else:
            self.assertEqual(data['deleted'], id)

    def test_create_question(self):
        data = json.dumps(question = {
            'question': 'How many african countries are there?',
            'answer': '54',
            'category': 1,
            'difficulty': 1
        })
        response = self.client().post('/questions', data=data, content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()