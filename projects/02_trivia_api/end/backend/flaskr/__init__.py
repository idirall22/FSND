import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category
from sqlalchemy.sql.expression import func
from werkzeug.exceptions import HTTPException, NotFound

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  

  
  @app.after_request
  def set_headers(response):
    """
    Add Access-Control-Allow-Headers and  Access-Control-Allow-Methods to response
    """
    response.headers.add('Access-Control-Allow-Headers',
                          'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods',
                          'GET, PATCH, POST, DELETE, OPTIONS')
    return response

  @app.route('/', methods=['GET'])
  def homepage():
    abort(500)

  ###
  @app.route('/categories', methods=['GET'])
  def get_all_categories():
    """
    GET request for all available categories
    Ex:
      GET /categories
    """
    allCategories = Category.query.all()
    categories = {}
    for category in allCategories:
        categories[category.id] = category.type
    return jsonify({
        'categories': categories
    })

  @app.route('/questions', methods=['GET'])
  def get_questions():
    """
    Get request for questions, categories, total number of total questions.
    Ex:
      GET /questions?page=1
    """
    page = int(request.args.get('page', '0'))
    offset = page * 10
    limit = offset + 10

    categories = {}
    all_categories = Category.query.all()
    for category in all_categories:
        categories[category.id] = category.type

    questions = [question.format() \
       for question in Question.query.limit(limit).offset(offset)]

    return jsonify({
        'questions': questions,
        'total_questions': len(questions),
        'categories': categories
    })
    
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    """
    Delete request for deleting a question by id
    Ex:
      DELETE /questions/1
    """
    question = Question.query.get(question_id)
    if not question:
        return abort(404, f'Question with id {question_id} not exists')
    
    question.delete()
    return jsonify({
        'deleted': question_id
    })

  @app.route('/questions', methods=['POST'])
  def create_question():
    """
    POST request to insert a question
    Ex:
      POST /questions
      body: {"question":"", "answer":"", category:1, difficulty:1}
    """
    question = request.json.get('question')
    if not question:
      return abort(400, "question field should not be empty")

    answer = request.json.get('answer')
    if not answer:
      return abort(400, "answer field should not be empty")

    category = request.json.get('category')
    if not category:
      return abort(400, "category field should not be empty")

    difficulty = request.json.get('difficulty')
    if not difficulty:
      return abort(400, "difficulty field should not be empty")

    new_question = Question(question, answer, category, difficulty)
    new_question.insert()
    return jsonify({
        'question': new_question.format()
    })

  @app.route('/search', methods=['POST'])
  def search():
    """
    POST request to search questions using the search term.
    Ex:
      POST /search
      body: {"q": ""}
    """
    search_term = request.json.get('q', '')

    if search_term == "":
      return jsonify({
          'error': 'search term should not be empty'
      })  
    
    
    allQuestions = Question.query.filter(
      Question.question.like("%" + search_term + "%"))
    questions = [question.format() for question in allQuestions]
    
    return jsonify({
        'questions': questions,
        'total_questions': len(questions),
        'current_categories': []
    })


  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    """
    GET request get questions by category.
    Ex:
      GET /categories/1/questions
    """
    questions = [question.format() for question in
                    Question.query.filter(Question.category == str(category_id))]
    
    return jsonify({
        'questions': questions,
        'total_questions': len(questions),
        'current_category': category_id
    })

  @app.route('/quizzes', methods=['POST'])
  def get_quizz_questions():
    """
    POST request get question for quizz.
    Ex:
      POST /quizzes
      body: {"previous_questions": [], "quiz_category": {"id":1}}
    """
    previous_questions = request.json.get('previous_questions')
    quiz_category = request.json.get('quiz_category')

    if not quiz_category:
        return abort(400, 'Required keys missing from request body')

    category_id = quiz_category.get('id')

    questions = Question.query.filter(
        Question.category == str(category_id), ~Question.id.in_(previous_questions))

    question = questions.order_by(func.random()).first()
    if not question:
        return jsonify({})
    return jsonify({
        'question': question.format()
    })

  @app.errorhandler(HTTPException)
  def http_exception_handler(error):
    """
    HTTP error handler for all endpoints
    """
    code = 500
    if isinstance(error, HTTPException):
        code = error.code

    return jsonify({'error': str(error), "code": code}), code

  return app

    