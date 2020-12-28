import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, db_drop_and_create_all, Actor, Movie, Performance, db_drop_and_create_all
# from config import bearer_tokens
from sqlalchemy import desc
from datetime import date

assistant_auth_header = {
    'Authorization': os.environ.get('ASSISTANT')
}

director_auth_header = {
    'Authorization': os.environ.get('DIRECTOR')
}

producer_auth_header = {
    'Authorization': os.environ.get('PRODUCER')
}

class AgencyTestCase(unittest.TestCase):
    """This class represents the agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.app = create_app()
        self.client = self.app.test_client
        dev_database_path = "postgres://{}:{}@localhost:{}/{}".format(
            os.environ.get("PG_USERNAME"),
            os.environ.get("PG_PASSWORD"),
            os.environ.get("PG_PORT"),
            os.environ.get("PG_DATABASE_NAME")
        )
        self.database_path = os.environ.get('DATABASE_URL', dev_database_path)

        setup_db(self.app, self.database_path)
        # db_drop_and_create_all()
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            # self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

#----------------------------------------------------------------------------#
# Tests for /actors POST
#----------------------------------------------------------------------------#
    def create_actor(self):
        json_create_actor = {
            'name' : 'bob',
            'age' : 25
        } 

        res = self.client().post('/actors',json = json_create_actor, headers = director_auth_header)
        return res, json.loads(res.data)

    def test_create_new_actor(self):
        """Test POST new actor."""

        # json_create_actor = {
        #     'name' : 'bob',
        #     'age' : 25
        # } 

        # res = self.client().post('/actors',json = json_create_actor, headers = director_auth_header)
        # data = json.loads(res.data)
        res, data = self.create_actor()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['created'], 1)
    
    def test_error_401_new_actor(self):
        """Test POST new actor w/o Authorization."""

        json_create_actor = {
            'name' : 'bob',
            'age' : 25
        } 
        res = self.client().post('/actors', json = json_create_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_error_422_create_new_actor(self):
        """Test Error POST new actor."""

        json_create_actor_without_name = {
            'age' : 25
        } 

        res = self.client().post('/actors', json = json_create_actor_without_name, headers = director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#
# Tests for /actors GET

    def test_get_all_actors(self):
        """Test GET all actors."""
        self.create_actor()
        res = self.client().get('/actors', headers = assistant_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

    def test_error_401_get_all_actors(self):
        """Test GET all actors w/o Authorization."""
        res = self.client().get('/actors?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_error_404_get_actors(self):
        """Test Error GET all actors."""
        res = self.client().get('/actors?page=999', headers = assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

#----------------------------------------------------------------------------#
# Tests for /actors PATCH
#----------------------------------------------------------------------------#

    def test_edit_actor(self):
        """Test PATCH existing actors"""
        self.create_actor()
        json_edit_actor_with_new_age = {
            'age' : 30
        } 
        res = self.client().patch('/actors/1', json = json_edit_actor_with_new_age, headers = director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actor']) > 0)
        self.assertEqual(data['updated'], 1)

    def test_error_400_edit_actor(self):
        """Test PATCH with non json body"""

        res = self.client().patch('/actors/123412', headers = director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_error_404_edit_actor(self):
        """Test PATCH with non valid id"""
        json_edit_actor_with_new_age = {
            'age' : 30
        } 
        res = self.client().patch('/actors/999', json = json_edit_actor_with_new_age, headers = director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

#----------------------------------------------------------------------------#
# Tests for /actors DELETE
#----------------------------------------------------------------------------#

    def test_error_401_delete_actor(self):
        """Test DELETE existing actor w/o Authorization"""
        self.create_actor()
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_error_403_delete_actor(self):
        """Test DELETE existing actor with missing permissions"""
        res = self.client().delete('/actors/1', headers = assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_delete_actor(self):
        """Test DELETE existing actor"""
        self.create_actor()
        res = self.client().delete('/actors/1', headers = director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], '1')

    def test_error_404_delete_actor(self):
        """Test DELETE non existing actor"""
        res = self.client().delete('/actors/15125', headers = director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

#----------------------------------------------------------------------------#
# Tests for /movies POST
#----------------------------------------------------------------------------#

    def create_movie(self):
        json_create_movie = {
            'title' : 'Titanic',
            'release_date' : date.today()
        } 

        res = self.client().post('/movies', json = json_create_movie, headers = producer_auth_header)
        data = json.loads(res.data)
        return res, data

    def test_create_new_movie(self):
        """Test POST new movie."""
        res, data = self.create_movie()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['created'], 1)

    def test_error_422_create_new_movie(self):
        """Test Error POST new movie."""

        json_create_movie_without_name = {
            'release_date' : date.today()
        } 

        res = self.client().post('/movies', json = json_create_movie_without_name, headers = producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

#----------------------------------------------------------------------------#
# Tests for /movies GET
#----------------------------------------------------------------------------#

    def test_get_all_movies(self):
        """Test GET all movies."""
        self.create_movie()
        res = self.client().get('/movies?page=1', headers = assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

    def test_error_401_get_all_movies(self):
        """Test GET all movies w/o Authorization."""
        res = self.client().get('/movies?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_error_404_get_movies(self):
        """Test Error GET all movies."""
        res = self.client().get('/movies?page=999', headers = assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

#----------------------------------------------------------------------------#
# Tests for /movies PATCH
#----------------------------------------------------------------------------#

    def test_edit_movie(self):
        """Test PATCH existing movies"""
        self.create_movie()
        json_edit_movie = {
            'release_date' : date.today()
        } 
        res = self.client().patch('/movies/1', json = json_edit_movie, headers = producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movie']) > 0)

    def test_error_400_edit_movie(self):
        """Test PATCH with non valid id json body"""
        res = self.client().patch('/movies/1', headers = producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_error_404_edit_movie(self):
        """Test PATCH with non valid id"""
        json_edit_movie = {
            'release_date' : date.today()
        } 
        res = self.client().patch('/movies/999', json = json_edit_movie, headers = producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

#----------------------------------------------------------------------------#
# Tests for /movies DELETE
#----------------------------------------------------------------------------#

    def test_error_401_delete_movie(self):
        """Test DELETE existing movie w/o Authorization"""
        self.create_movie()
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_error_403_delete_movie(self):
        """Test DELETE existing movie with wrong permissions"""
        res = self.client().delete('/movies/1', headers = assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_delete_movie(self):
        """Test DELETE existing movie"""
        self.create_movie()
        res = self.client().delete('/movies/1', headers = producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], '1')

    def test_error_404_delete_movie(self):
        """Test DELETE non existing movie"""
        res = self.client().delete('/movies/999', headers = producer_auth_header) 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

if __name__ == "__main__":
    unittest.main()