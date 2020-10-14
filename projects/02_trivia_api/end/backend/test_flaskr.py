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
        self.database_name = "trivia"
        self.database_path = "postgres://postgres:password@{}/{}".format('localhost:5432', self.database_name)
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

    def test_create_question_success(self):
        data = json.dumps({
            'question': 'How many african countries are there?',
            'answer': '54',
            'category': 1,
            'difficulty': 1
        })
        response = self.client().post('/questions', data=data, content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_create_question_fail(self):
        data = json.dumps({
            'question': 'How many african countries are there?',
            'answer': '54',
            # 'category': 1,
            'difficulty': 1
        })
        response = self.client().post('/questions', data=data, content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)


    def test_delete_question_success(self):
            id = 5
            response = self.client().delete(f"/questions/{id}")
            data = json.loads(response.data)

            if response.status_code == 404:
                self.assertEqual(data['code'], 404)
            else:
                self.assertEqual(data['deleted'], id)
    
    def test_search(self):
        data = {'q': 'How'}
        response = self.client().post('/search', data=json.dumps(data), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        
    def test_get_quiz_questions(self):
        request_data = {
            'previous_questions': [1, 2, 3, 4],
            'quiz_category': {'id': 1, 'type': 'Science'}
        }
        response = self.client().post('/quizzes', data=json.dumps(request_data),
                                content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        if data.get('question', None):
            self.assertNotIn(data['question']['id'],
                            request_data['previous_questions'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()