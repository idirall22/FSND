# Capston

## Getting Started

#### Steps to run the tests localhost:
- **Host: http://localhost:5000**
1. make env `generate env`  
2. source env/bin/activate
3. make install `install requirements.txt file`
4. make postgres-up `create postgres container`
5. make run `start the server`
6. make test `run all the tests`
7. make postgres-down `delete postgres container`

#### Steps to run the tests localhost:
- **Host: https://idir-capston.herokuapp.com/**

### Producer Actions:

## Curl Create an actor
```js
curl -X POST -H "Content-type: application/json" -H "Authorization: bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1xMktwY1Q5WU9nSjE2Ml92cDZ1NyJ9.eyJpc3MiOiJodHRwczovL2Rldi05MnB2Z2t3My5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZkYTVkMTU0NWEyZjUwMDZlZTA3NjQwIiwiYXVkIjoiY2Fwc3RvbiIsImlhdCI6MTYwODM4MTc1MiwiZXhwIjoxNjA4NDY4MTUyLCJhenAiOiJqVHAzMERvWUx2Z2ZPUTJrbjBPa1N4Z0J1b095cTRiQSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9ycyIsImNyZWF0ZTptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImVkaXQ6YWN0b3JzIiwiZWRpdDptb3ZpZXMiLCJyZWFkOmFjdG9ycyIsInJlYWQ6bW92aWVzIl19.sZCc0qVOwtIy8nXbNuL2M8tJ05zzV0fBkChWrIMht4XANIW6x8R_nnak-_MJWVs-Pszj-6lPtradIl6PGByWd6DJSBQ-LOs3CKAr0gFrtEcIqWgvSX1gY7jWhBP0BGeWd_bYCDWJMrMmr39VhjnbVsg0-LoCnv3AuhOFpWuieET3ct3FfnJxgbCLHJYTW-vIPaLpcJyukWmS--OGYUX4Eibc4yrtd1BIwO2iSxq0yazTL-F0_3e2IM0pzHQzpw6MJhG446f9zPePkdfEYD-fE4-sRcL3H5sIHd6NxIpbk1nGxM9eUNpBleuzWkF79MxYGr7G2iuPUSSLrspolrb_vQ" -d '{"name": "jack", "age": 25}' https://idir-capston.herokuapp.com/actors
```

## Curl Get a list of actors
```js
curl -H "Authorization: bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1xMktwY1Q5WU9nSjE2Ml92cDZ1NyJ9.eyJpc3MiOiJodHRwczovL2Rldi05MnB2Z2t3My5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZkYTVjYzNjMDgzNDQwMDY4YjgwZTgwIiwiYXVkIjoiY2Fwc3RvbiIsImlhdCI6MTYwODM4MTI3NiwiZXhwIjoxNjA4NDY3Njc2LCJhenAiOiJqVHAzMERvWUx2Z2ZPUTJrbjBPa1N4Z0J1b095cTRiQSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.DCcgHX-Y19wtb5s47cP_jjIr4snw0mMel2rkEcsLIyMbGjGc9jNel_OdhnB2_Hoa8gNwJpYgXMh2ymkw-coHtGMOPVyN-iYAD7DGgsqLnNZXmQan9bCFM-KDuzg6op7zyvktZ9Uu3-8fi68POucGHmfw1KG5REjZXcRl8aE8u-j6N1yfvRkzy-s0NapZcQ96X6ftQstajrwgoUMu4b1PhnlYlXnYLNt6cqGI2vPvklrUgD_fNvzcQoMnn1rbpxRsiWQ67CFbUUg0fXwsRAJ8IkKAOXrlwCd7bGaLrPeToEEHs-oxgLfiU0AfI-Hj1pDOdK0jg7KBq0ukIJLyQGimUA" https://idir-capston.herokuapp.com/actors
```

## Curl PATCH an actors
```js
curl -X PATCH -H "Content-type: application/json" -H "Authorization: bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1xMktwY1Q5WU9nSjE2Ml92cDZ1NyJ9.eyJpc3MiOiJodHRwczovL2Rldi05MnB2Z2t3My5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZkYTVkMTU0NWEyZjUwMDZlZTA3NjQwIiwiYXVkIjoiY2Fwc3RvbiIsImlhdCI6MTYwODM4MTc1MiwiZXhwIjoxNjA4NDY4MTUyLCJhenAiOiJqVHAzMERvWUx2Z2ZPUTJrbjBPa1N4Z0J1b095cTRiQSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9ycyIsImNyZWF0ZTptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImVkaXQ6YWN0b3JzIiwiZWRpdDptb3ZpZXMiLCJyZWFkOmFjdG9ycyIsInJlYWQ6bW92aWVzIl19.sZCc0qVOwtIy8nXbNuL2M8tJ05zzV0fBkChWrIMht4XANIW6x8R_nnak-_MJWVs-Pszj-6lPtradIl6PGByWd6DJSBQ-LOs3CKAr0gFrtEcIqWgvSX1gY7jWhBP0BGeWd_bYCDWJMrMmr39VhjnbVsg0-LoCnv3AuhOFpWuieET3ct3FfnJxgbCLHJYTW-vIPaLpcJyukWmS--OGYUX4Eibc4yrtd1BIwO2iSxq0yazTL-F0_3e2IM0pzHQzpw6MJhG446f9zPePkdfEYD-fE4-sRcL3H5sIHd6NxIpbk1nGxM9eUNpBleuzWkF79MxYGr7G2iuPUSSLrspolrb_vQ" -d '{"name": "jack2", "age": 27}' https://idir-capston.herokuapp.com/actors/1
```

## Curl DELETE an actors
```js
curl -X DELETE -H "Content-type: application/json" -H "Authorization: bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1xMktwY1Q5WU9nSjE2Ml92cDZ1NyJ9.eyJpc3MiOiJodHRwczovL2Rldi05MnB2Z2t3My5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZkYTVkMTU0NWEyZjUwMDZlZTA3NjQwIiwiYXVkIjoiY2Fwc3RvbiIsImlhdCI6MTYwODM4MTc1MiwiZXhwIjoxNjA4NDY4MTUyLCJhenAiOiJqVHAzMERvWUx2Z2ZPUTJrbjBPa1N4Z0J1b095cTRiQSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9ycyIsImNyZWF0ZTptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImVkaXQ6YWN0b3JzIiwiZWRpdDptb3ZpZXMiLCJyZWFkOmFjdG9ycyIsInJlYWQ6bW92aWVzIl19.sZCc0qVOwtIy8nXbNuL2M8tJ05zzV0fBkChWrIMht4XANIW6x8R_nnak-_MJWVs-Pszj-6lPtradIl6PGByWd6DJSBQ-LOs3CKAr0gFrtEcIqWgvSX1gY7jWhBP0BGeWd_bYCDWJMrMmr39VhjnbVsg0-LoCnv3AuhOFpWuieET3ct3FfnJxgbCLHJYTW-vIPaLpcJyukWmS--OGYUX4Eibc4yrtd1BIwO2iSxq0yazTL-F0_3e2IM0pzHQzpw6MJhG446f9zPePkdfEYD-fE4-sRcL3H5sIHd6NxIpbk1nGxM9eUNpBleuzWkF79MxYGr7G2iuPUSSLrspolrb_vQ" https://idir-capston.herokuapp.com/actors/1
```

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