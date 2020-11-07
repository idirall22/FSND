# Coffee Shop Backend

## Getting Started

- **Host: http://localhost:5000**

#### Steps to run the backend on localhost:
1. make env `generate env`  
2. source env/bin/activate
3. make install `install requirements.txt file`
4. make run `start the server`

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

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 2 users - assign the Barista role to one and Manager role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
    - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`

## Endpoints
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

### GET/drinks
- **General**
    * Return a list of drinks.
    * Auth not required
- **Sample**
    * `http://127.0.0.1:5000/drinks`

```js
response:
    {
        "success" True,
        "drinks":[
            {
                "success": True,
                "drinks": {
                    "title": "drink_name",
                    "recips": [
                        {
                            "color": "xxx",
                            "parts": 1
                        }
                    ],
                }
            },
            {
                "success": True,
                "drinks": {
                    "title": "drink_name",
                    "recips": [
                        {
                            "color": "xxx",
                            "parts": 1
                        }
                    ],
                }
            }
        ]
    }
```
### GET/drinks-detail
- **General**
    * Return a full detailed list of drinks.
    * Auth required `get:drinks-detail`
- **Sample**
    * `http://127.0.0.1:5000/drinks-detail`

```js
response:
    {
        "success" True,
        "drinks":[
            {
                "success": True,
                "drinks": {
                    "title": "drink_name",
                    "recips": [
                        {
                            "name": "xxx",
                            "color": "xxx",
                            "parts": 1
                        }
                    ],
                }
            },
            {
                "success": True,
                "drinks": {
                    "title": "drink_name",
                    "recips": [
                        {
                            "name": "xxx",
                            "color": "xxx",
                            "parts": 1
                        }
                    ],
                }
            }
        ]
    }
```

### POST/drinks
- **General**
    * Create a drink.
    * Auth required `post:drinks`
- **Sample**
    * `http://127.0.0.1:5000/drinks`

```js
request:
    {
        "title": "xxx",
        "recips": [
            {
                "name": "xxx",
                "color": "xxx",
                "parts": 1
            }
        ]
    }
response: 
    {   
        "success": True,
        "drink":{
            "id": 1,
            "title": "xxx",
            "recips": [
                {
                    "name": "xxx",
                    "color": "xxx",
                    "parts": 1
                }
            ]
        }
    }
```

### PATCH/drinks/<drink_id>
- **General**
    * Update a drink.
    * Auth required `patch:drinks`
- **Sample**
    * `http://127.0.0.1:5000/drinks/1`

```js
request:
    {
        "title": "xxx",
        "recips": [
            {
                "name": "xxx",
                "color": "xxx",
                "parts": 1
            }
        ]
    }
response: 
    {   
        "success": True,
        "drink":{
            "id": 1,
            "title": "xxx",
            "recips": [
                {
                    "name": "xxx",
                    "color": "xxx",
                    "parts": 1
                }
            }
        ]
    }
```

### DELETE/drinks/<drink_id>
- **General**
    * Delete a drink.
    * Auth required `delete:drinks`
- **Sample**
    * `http://127.0.0.1:5000/drinks/1`

```js
response: 
    {
        'success': True,
        'delete': 1
    }
```