import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie
import json
from auth import AuthError, requires_auth

pagination = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  setup_db(app)

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response

  # ----------------------------------------------------------------
  # Actor
  # ----------------------------------------------------------------

  # List actors
  @app.route('/actors', methods=['GET'])
  @requires_auth('read:actors')
  def get_actors(payload):
    """Returns paginated actors object"""

    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * pagination
    end = start + pagination
    
    actors = Actor.query.all()
    actors_formatted = [act.format() for act in actors]

    if len(actors_formatted) == 0:
      abort(404, {'message': 'no actors found.'})

    return jsonify({
      'success': True,
      'actors': actors_formatted[start:end]
    })
  
  # Create an actor.
  @app.route('/actors', methods=['POST'])
  @requires_auth('create:actors')
  def create_actor(payload):
    """Inserts a new Actor"""

    # Get request json
    body = request.get_json()

    if not body:
          abort(400, {'message': 'invalid request.'})

    # Get name
    name = body.get('name', None)
    if not name:
      abort(422, {'message': 'name should not be empty.'})
    
    # Get age
    age = body.get('age', None)
    if not age:
      abort(422, {'message': 'age should not be empty.'})

    # Get gender
    gender = body.get('gender', 'Other')

    # Create Actor
    actor = (Actor(
          name = name, 
          age = age,
          gender = gender
          ))
    # Insert Actor
    actor.insert()

    return jsonify({
      'success': True,
      'created': actor.id
    })

  # Update an actor.
  @app.route('/actors/<actor_id>', methods=['PATCH'])
  @requires_auth('edit:actors')
  def edit_actors(payload, actor_id):
    """Edit an existing Actor"""
    
    # Get request json
    body = request.get_json()

    # Check if actor id is not provided
    if not actor_id:
      abort(400, {'message': 'actor id "{}" not valid.'.format(actor_id)})

    if not body:
      abort(400, {'message': 'invalid request.'})

    # Query actor from database
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

    # Check if actor exists.
    if not actor:
      abort(404, {'message': 'Actor with id {} not exists.'.format(actor_id)})

    # Update actor data.
    actor.name = body.get('name', actor.name)
    actor.age = body.get('age', actor.age)
    actor.gender = body.get('gender', actor.gender)
    actor.update()

    return jsonify({
      'success': True,
      'updated': actor.id,
      'actor' : [actor.format()]
    })


  @app.route('/actors/<actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actors(payload, actor_id):
    """Delete an existing Actor"""

    # Check if actor id is not provided
    if not actor_id:
      abort(400, {'message': 'actor id "{}" not valid.'.format(actor_id)})

    # Query actor from database
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

    # Check if actor exists.
    if not actor:
      abort(404, {'message': 'Actor with id {} not exists.'.format(actor_id)})
      
    # Delete actor from database
    actor.delete()
    
    return jsonify({
      'success': True,
      'deleted': actor_id
    })

  # ----------------------------------------------------------------
  # Movie
  # ----------------------------------------------------------------

  @app.route('/movies', methods=['GET'])
  @requires_auth('read:movies')
  def get_movies(payload):
    """Returns paginated movies object"""

    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * pagination
    end = start + pagination

    movies = Movie.query.all()
    if len(movies) == 0:
      abort(404, {'message': 'no movies found in database.'})

    movies_formatted = [mov.format() for mov in movies]

    return jsonify({
      'success': True,
      'movies': movies_formatted[start:end]
    })

  @app.route('/movies', methods=['POST'])
  @requires_auth('create:movies')
  def insert_movies(payload):
    """Inserts a new movie"""

    # Get request json
    body = request.get_json()

    if not body:
          abort(400, {'message': 'invalid request.'})

    title = body.get('title', None)
    if not title:
      abort(422, {'message': 'title not provided.'})

    release_date = body.get('release_date', None)
    if not release_date:
      abort(422, {'message': 'release_date not provided.'})

    # Insert movie.
    movie = (Movie(
      title = title, 
      release_date = release_date
    ))
    movie.insert()

    return jsonify({
      'success': True,
      'created': movie.id
    })

  @app.route('/movies/<movie_id>', methods=['PATCH'])
  @requires_auth('edit:movies')
  def edit_movies(payload, movie_id):
    """Edit an existing Movie"""
    
    # Get request json
    body = request.get_json()

    # Check if actor id is not provided
    if not movie_id:
      abort(400, {'message': 'movie id "{}" not valid.'.format(movie_id)})

    if not body:
      abort(400, {'message': 'invalid request.'})

    # Query Movie from database
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

    # Check if Movie exists.
    if not movie:
      abort(404, {'message': 'Movie with id {} not exists.'.format(movie_id)})

    # Update movie.
    movie.title = body.get('title', movie.title)
    movie.release_date = body.get('release_date', movie.release_date)
    movie.update()

    return jsonify({
      'success': True,
      'edited': movie.id,
      'movie' : [movie.format()]
    })

  @app.route('/movies/<movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movies(payload, movie_id):
    """Delete an existing Movie"""

    # Check if movie id is not provided
    if not movie_id:
      abort(400, {'message': 'movie id "{}" not valid.'.format(movie_id)})

    # Query movie from database
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

    # Check if movie exists.
    if not movie:
      abort(404, {'message': 'movie with id {} not exists.'.format(movie_id)})
      
    # Delete movie from database
    movie.delete()
    
    return jsonify({
      'success': True,
      'deleted': movie_id
    })

    # ----------------------------------------------------------------
    # Error Handlers
    # ----------------------------------------------------------------

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                        "success": False, 
                        "error": 422,
                        "message": get_error_message(error,"unprocessable")
                        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
                        "success": False, 
                        "error": 400,
                        "message": get_error_message(error, "bad request")
                        }), 400

    @app.errorhandler(404)
    def ressource_not_found(error):
        return jsonify({
                        "success": False, 
                        "error": 404,
                        "message": get_error_message(error, "resource not found")
                        }), 404

    @app.errorhandler(AuthError)
    def authentification_failed(AuthError): 
        return jsonify({
                        "success": False, 
                        "error": AuthError.status_code,
                        "message": AuthError.error['description']
                        }), AuthError.status_code


  return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)