import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_all_drinks():
    page = int(request.args.get('page', '0'))
    offset = page * 10
    limit = offset + 10
    
    drinks = [drink.short() \
       for drink in Drink.query.limit(limit).offset(offset)]
    if not drinks:
        return abort(404)

    return jsonify({
        'success': True,
        'drinks': drinks
    }), 200

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth("get:drinks-detail")
def get_all_drinks_detail(jwt):
    page = int(request.args.get('page', '0'))
    offset = page * 10
    limit = offset + 10
    
    drinks = [drink.long() \
       for drink in Drink.query.limit(limit).offset(offset)]
    if not drinks:
        return abort(404)

    return jsonify({
        'success': True,
        'drinks': drinks
    }), 200

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth("post:drinks")
def create_drink(jwt):

    if request.json == None:
        return abort(400)

    title = request.json.get('title')
    if not title:
        return abort(400)

    recipe = request.json.get('recipe')
    if not recipe:
        return abort(400)

    new_drink = Drink(title, json.dumps(recipe))
    new_drink.insert()

    return jsonify({
        'success': True,
        'drink': new_drink.long()
    }), 200

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth("patch:drinks")
def update_drink(jwt, drink_id):

    if request.json == None:
        return abort(400)

    drink = Drink.query.get(drink_id)
    if not drink:
        return abort(404)

    title = request.json.get('title')
    recipe = request.json.get('recipe')

    if not title and not recipe:
        abort(400)

    if title:
        drink.title = title
      
    if recipe:
        drink.recipe = json.dumps(recipe)

    drink.update()

    return jsonify({
        'success': True,
        'drink': drink.long()
    }), 200

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['Delete'])
@requires_auth("delete:drinks")
def delete_drink(jwt, drink_id):
    drink = Drink.query.get(drink_id)
    if not drink:
        return abort(404)
    
    drink.delete()
    return jsonify({
        'success': True,
        'delete': drink_id
    }), 200

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(404)
def not_exists(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "not exists"
                    }), 404

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
                    "success": False, 
                    "error": 401,
                    "message": "unauthorized"
                    }), 401

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
                    "success": False, 
                    "error": 400,
                    "message": "bad request"
                    }), 400
