# Capston

## Getting Started
### Motivation for the project
The Agency project is a Rest API built using python3 and flask, it allows to manage an agency using an RBAC access control, and permit to management actors and movies.

### Steps to run the tests localhost:
- **Host: http://localhost:5000**
1. make env `generate env`  
2. run `source ./setup.sh`
3. make install `install requirements.txt file`
4. make postgres-up `create postgres container`
5. make run `start the server`
6. make test `run all the tests`
7. make postgres-down `delete postgres container`

### Steps to run the tests localhost:
- **Host: https://idir-capston.herokuapp.com/**

### Producer Actions:

## Curl Create an actor
```js
curl -X POST -H "Content-type: application/json" -H "Authorization: $PRODUCER" -d '{"name": "jack", "age": 25}' https://idir-capston.herokuapp.com/actors
```

## Curl Get a list of actors
```js
curl -H "Authorization: $PRODUCER" https://idir-capston.herokuapp.com/actors
```

## Curl PATCH an actors
```js
curl -X PATCH -H "Content-type: application/json" -H "Authorization: $PRODUCER" -d '{"name": "jack2", "age": 27}' https://idir-capston.herokuapp.com/actors/1
```

# Generate JWT:
You can use this url to generate JWT:
`https://dev-92pvgkw3.eu.auth0.com/authorize?audience=capston&response_type=token&client_id=jTp30DoYLvgfOQ2kn0OkSxgBuoOyq4bA&redirect_uri=http://loclalhost:5000/`

## Curl DELETE an actors
```js
curl -X DELETE -H "Content-type: application/json" -H "Authorization: " https://idir-capston.herokuapp.com/actors/1
```

### Credentials:
- assistant:
    1. Email: assistant@email.com
    2. Password: 1assistant*/
- producer:
    1. Email: producer@email.com
    2. Password: 1producer*/
- director
    1. Email: director@email.com
    2. Password: 1Director*/
    
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

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Endpoints

## Permissions (RBAC)
The API uses RBAC for access control:
- assistant: 
    * read:actors
    * read:movies
- producer:
    * read:actors
    * edit:actors	
    * create:actors
    * delete:actors	
    * read:movies
    * create:movies
    * edit:movies
    * delete:movies	
- director:
    * read:actors
    * read:movies
    * create:actors
    * delete:actors	
    * edit:actors	
    * edit:movies

### Getting Started
- Base URL: `http://127.0.0.1:5000/`
- Authentication: require auth.

### Error Handling
- Error are returned as JSON object in the following format:
```js
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

- The API will return two error when request fails:
    * 400: Bad Request
    * 401: unauthorized
    * 404: Ressource Not Found
    * 422: unprocessable

### GET/actors
- **General**
    * Return a list of actors.
    * permission required `read:actors`
- **Sample**
    * `http://127.0.0.1:5000/actors`

```js
response:
    {
        "success" True,
        "actors":[
            {
                "id": 1,
                "name": "alex",
                "gender": "male",
                "age": 20
            }
        ]
    }
```

### POST/actors
- **General**
    * Create a actor.
    * permission required `create:actors`
- **Sample**
    * `http://127.0.0.1:5000/actors`

```js
request:
    {
        "name": "xxx",
        "gender": "xxx",
        "age": 25,
    }
response: 
    {   
        "success": True,
        "created": 1
    }
```

### PATCH/actors/<actor_id>
- **General**
    * Update a actor.
    * Permission required `edit:actor`
- **Sample**
    * `http://127.0.0.1:5000/actors/1`

```js
request:
    {
        "name": "xxx",
        "gender": "xxx",
        "age": 25,
    }
response: 
    {   
        "success": True,
        "actor":{
            "id": 1,
            "name": "xxx",
            "gender": "xxx",
            "age": 25
        }
    }
```

### DELETE/actors/<actor_id>
- **General**
    * Delete an actor.
    * Permission required `delete:actors`
- **Sample**
    * `http://127.0.0.1:5000/actors/1`

```js
response: 
    {
        'success': True,
        'deleted': 1
    }
```

### GET/movies
- **General**
    * Return a list of movies.
    * permission required `read:movies`
- **Sample**
    * `http://127.0.0.1:5000/movies`

```js
response:
    {
        "success" True,
        "movies":[
            {
                "id" : 1
                "title" : "xxx"
                "release_date" : "xxx"
            }
        ]
    }
```

### POST/movies
- **General**
    * Create a movie.
    * permission required `create:movies`
- **Sample**
    * `http://127.0.0.1:5000/movies`

```js
request:
    {
        "title": "xxx",
        "release_date": "xxx",
    }
response: 
    {   
        "success": True,
        "created": 1
    }
```

### PATCH/movies/<movie_id>
- **General**
    * Update a movie.
    * Permission required `edit:movie`
- **Sample**
    * `http://127.0.0.1:5000/movies/1`

```js
request:
    {
        "title": "xxx",
        "release_date": "xxx"
    }
response: 
    {   
        "success": True,
        "actor":{
            "id": 1,
            "title": "xxx",
            "release_date": "xxx"
        }
    }
```

### DELETE/movies/<movie_id>
- **General**
    * Delete a movie.
    * Permission required `delete:movies`
- **Sample**
    * `http://127.0.0.1:5000/movies/1`

```js
response: 
    {
        'success': True,
        'deleted': 1
    }
```