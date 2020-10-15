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
    
    def test_get_all_categories_success(self):
        response = self.client().get('/categories')
        self.assertEqual(response.status_code, 200)

    def test_get_all_categories_fail(self):
        response = self.client().get('/categories')
        self.assertEqual(response.status_code, 200)

    def test_get_questions_success(self):
        response = self.client().get('/questions?page=1')
        self.assertEqual(response.status_code, 200)
    
    def test_get_questions_fail(self):
        response = self.client().get('/questions?page=10')
        self.assertEqual(response.status_code, 404)

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
        if not data["success"]:
            self.assertEqual(response.status_code, 404)
        else:
            self.assertEqual(data['deleted'], id)

    def test_delete_question_fail(self):
        id = 1000
        response = self.client().delete(f"/questions/{id}")
        data = json.loads(response.data)
        self.assertEqual(data['code'], 404)
    
    def test_search_success(self):
        data = {'q': 'How'}
        response = self.client().post('/search', data=json.dumps(data), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_search_fail(self):
        response = self.client().post('/search', data={}, content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)

    def test_get_questions_by_category_success(self):
        id = 1
        response = self.client().get(f'/categories/{id}/questions', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_questions_by_category_fail(self):
        id = 1000
        response = self.client().get(f'/categories/{id}/questions', content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_get_quiz_questions_success(self):
        request_data = {
            'previous_questions': [1, 2, 3, 4],
            'quiz_category': {'id': 1, 'type': 'Science'}
        }
        response = self.client().post('/quizzes', data=json.dumps(request_data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_quiz_questions_fail(self):
        request_data = {
            'previous_questions': [1, 2, 3, 4],
            'quiz_category': {}
        }
        response = self.client().post('/quizzes', data=json.dumps(request_data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()