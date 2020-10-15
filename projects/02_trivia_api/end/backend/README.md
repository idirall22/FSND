# Full Stack Trivia API Backend

## Getting Started

## Runing the Server:

- **start server**
1. make env 
2. source env/bin/activate
3. make install
4. make postgres-up
5. make populate
6. make run

- **run tests**
1. source env/bin/activate
2. make test

- **clean postgres database**
1. make postgres-down

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## Endpoints
### Getting Started
- Base URL: `http://127.0.0.1:5000/`
- Authentication: Does not require any auth.

### Error Handling
- Error are returned as JSON object in the following format:
```js
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

- The API will return three error when request fails:
    * 400: Bad Request
    * 404: Ressource Not Found
    * 422: Not Processable


### GET/categories
- **General**
    * Return a list of categories.
    * Result are paginates in groups of 10.
- **Sample**
    * `http://127.0.0.1:5000/categories`
    * `http://127.0.0.1:5000/categories?page=2`

```js
    "categories":[
        {
            "id": 1,
            "type": "Sport"
        },
        {
            "id": 2,
            "type": "History"
        }
    ]
```

### POST/questions
- **General**
    * Create a question.
- **Sample**
    * `http://127.0.0.1:5000/questions`
    * `curl -X POST -H "Content-Type: application/json" -d '{"question":"simple", "answer":"simple", category:1, difficulty:1}' 127.0.0.1:5000/questions`

- **Request body**
```js
    {
        "question":"simple",
        "answer":"simple",
        category:1,
        difficulty:1
    }
```
- **Response body**
```js
    {
        id: 11,
        "question":"simple",
        "answer":"simple",
        category:1,
        difficulty:1
    }
```

### DELETE/questions
- **General**
    * Delete a question by ID.
- **Sample**
    * `http://127.0.0.1:5000/questions`
    * `curl -X DELETE -H "Content-Type: application/json" 127.0.0.1:5000/questions/11`
- **Response body**
```js
    {
        "deleted": 11
    }
```


### POST/search
- **General**
    * Search a question by search term.
- **Sample**
    * `http://127.0.0.1:5000/search`
    * `curl -X POST -H "Content-Type: application/json" -d '{"q": "who"}' 127.0.0.1:5000/search`
- **Request body**
```js
    {
        "q": "Who"
    }
```
- **Response body**
```js
    {   
        "total_questions": 2,
        "current_categories": [],
        "questions":[
            {
                id: 1,
                "question":"question 1",
                "answer":"answer 1",
                category:1,
                difficulty:1
            },
            {
                id: 2,
                "question":"question 2",
                "answer":"answer 2",
                category:2,
                difficulty:3
            }
        ]
    }
```

### GET/categories/<int:category_id>/questions
- **General**
    * Return questions by category id.
- **Sample**
    * `http://127.0.0.1:5000/categories/1/questions`
    * `curl -H "Content-Type: application/json" 127.0.0.1:5000/categories/1/questions`
- **Response body**
```js
    {   
        "total_questions": 2,
        "current_category": 1,
        "questions":[
            {
                id: 1,
                "question":"question 1",
                "answer":"answer 1",
                category:1,
                difficulty:1
            },
            {
                id: 2,
                "question":"question 2",
                "answer":"answer 2",
                category:1,
                difficulty:3
            }
        ]
    }
```

### POST/quizzes
- **General**
    * Return a random question by category id.
- **Sample**
    * `http://127.0.0.1:5000/categories/1/questions`
    * `curl -H "Content-Type: application/json" 127.0.0.1:5000/categories/1/questions`

- **Response body**
```js
    {
        "previous_questions":[1,2],
        "quiz_category":{
            "id": 1,
            'type': 'Science'
        }
    }

```
- **Response body**
```js
    {   
        "question":{
            id: 3,
            "question":"question 1",
            "answer":"answer 1",
            category:1,
            difficulty:1
        }
    }
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```