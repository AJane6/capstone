# My Full Stack Developer Capstone Project

Hello world. This API is my fifth ever project and I want to tell you why it's awesome.

This API lets the user manage a casting agency service, and match actors to movies. The three different levels of user have appropriate permissions in relation to the local POSTGRES database, using Auth0 for authentication of users, and heroku for deploying to the cloud.
The purpose of this API is to pass the final Udacity Full Stack Developer course! And to give the user casting agency service, of course.

I'll walk through setup and testing before giving a detailed breakdown of the endpoints. 

## Getting Started

Please note that all of this README assumes the user is working in Git Bash on a Windows machine. Also, the backend code here should follow PEP8 style.

### Installing Dependencies

#### Python 3.7

Make sure you have most up-to-date version of Python 3.7, or else some dependencies might not act as anticipated. Find out what your version is by running:

```
python --version
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

I will from now on assume that the user has a working knowledge of these dependencies.

## Database Setup
If deploying locally, the user should create a database called 'heroku'. We use Heroku to provide a cloud-hosted database otherwise.

#### Virtual Enviornment

Work in a virtual environment. This is sort of like making a copy of all the bits of Python that you need to run your project, and it's good practice to use it. Make sure you have installed the virtualenv library in the appropriate directory:

```
python install virtualenv
```

Then, create a virtual environment named 'venv' in the folder and activate the virtual environment:

```
virtualenv venv
source venv/scripts/activate
```

If you are going to stop using the app, simply deactivate the virtual environment:

```bash
deactivate
```

## Running the server

Navigate to the backend folder and, in a virtual environment, run the server by executing the following:

```
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

The first command tells the program where to fund our application, and the second tells the program to run in development mode. Meaning, it reloads every time we hit save (we don't have to restart the server manually each time) and we save a lot of development time. The application runs on https://castappajr.herokuapp.com/ if not running locally.  


## Testing
We can run our tests by simply running our Postman collection. Check it out to make sure you understand it, then run the test suite. 

Alternatively, we can run our entire test suite by running the following command at command line:
```
dropdb test_heroku
createdb test_heroku
psql -d test_heroku -U postgres -a -f test_heroku.psql
python test_app.py
```


# Detailed Breakdown of Endpoints - API Reference

## Error Handling

We return errors as JSON objects like in the following example:
```
{
    "success": False,
    "error": 400,
    "message": "bad request"

}
```

The user can expect to see these four errors in our API:
- [400] bad request
- [401] unauthorized
- [404] resource not found
- [422] unprocessable entity
- [500] internal server error

In short, the first three errors will be to do with user input, so if you see any of these, just check that you're inputting exactly what you mean to! If you see a 500 error, that'll require some more investigation. 

## Endpoints

### GET /actors
- [Permissions] Casting Assistant, Casting Director and Executive Producer.
- [General] Returns all actors in our database, but paginated so we only display a desirable number of them at once in order to keep the page loading as quickly as possible. The user can see a success status, the actors in the database, and the total number of actors. We paginate to 12 actors per page but the user can update the variable RESULTS_PER_PAGE to change this as desired.

```
{
  "actors": [
    {
      "age": 27,
      "gender": "Female",
      "id": 3,
      "name": "Magnolia"
    },
    {
      "age": 27,
      "gender": "Female",
      "id": 5,
      "name": "Magnolia"
    },
    {
      "age": 27,
      "gender": "Female",
      "id": 9,
      "name": "Magnolia"
    },
    {
      "age": 27,
      "gender": "Female",
      "id": 14,
      "name": "Magnolia"
    },
    {
      "age": 27,
      "gender": "Female",
      "id": 16,
      "name": "Magnolia"
    },
    {
      "age": 27,
      "gender": "Female",
      "id": 17,
      "name": "Magnolia"
    },
    {
      "age": 27,
      "gender": "Female",
      "id": 22,
      "name": "Magnolia"
    },
    {
      "age": 27,
      "gender": "Female",
      "id": 23,
      "name": "Magnolia"
    },
    {
      "age": 27,
      "gender": "Female",
      "id": 24,
      "name": "Magnolia"
    },
    {
      "age": 27,
      "gender": "Female",
      "id": 25,
      "name": "Magnolia"
    },
    {
      "age": 27,
      "gender": "Female",
      "id": 26,
      "name": "Magnolia"
    },
    {
      "age": 27,
      "gender": "Female",
      "id": 27,
      "name": "Magnolia"
    }
  ],
  "success": true,
  "total_actors": 91
}
```

### GET /movies
- [Permissions] Casting Assistant, Casting Director and Executive Producer.
- [General] Returns all movies in our database, also paginated. The user can see a success status, the movies in the database, and the total number of movies.

```
{
  "movies": [
    {
      "id": 4,
      "release_date": "Sun, 31 May 2020 00:00:00 GMT",
      "title": "Mi Vida"
    },
    {
      "id": 6,
      "release_date": "Sun, 31 May 2020 00:00:00 GMT",
      "title": "Mi Vida"
    },
    {
      "id": 7,
      "release_date": "Sun, 31 May 2020 00:00:00 GMT",
      "title": "Mi Vida"
    },
    {
      "id": 8,
      "release_date": "Sun, 31 May 2020 00:00:00 GMT",
      "title": "Mi Vida"
    },
    {
      "id": 9,
      "release_date": "Sun, 31 May 2020 00:00:00 GMT",
      "title": "Mi Vida"
    },
    {
      "id": 11,
      "release_date": "Sun, 31 May 2020 00:00:00 GMT",
      "title": "Lessons"
    },
    {
      "id": 12,
      "release_date": "Sun, 31 May 2020 00:00:00 GMT",
      "title": "Mi Vida"
    },
    {
      "id": 13,
      "release_date": "Sun, 31 May 2020 00:00:00 GMT",
      "title": "Mi Vida"
    },
    {
      "id": 14,
      "release_date": "Sun, 31 May 2020 00:00:00 GMT",
      "title": "Lessons"
    },
    {
      "id": 15,
      "release_date": "Sun, 31 May 2020 00:00:00 GMT",
      "title": "Mi Vida"
    },
    {
      "id": 17,
      "release_date": "Sun, 31 May 2020 00:00:00 GMT",
      "title": "Lessons"
    },
    {
      "id": 18,
      "release_date": "Sun, 31 May 2020 00:00:00 GMT",
      "title": "Mi Vida"
    }
  ],
  "success": true,
  "total_movies": 12
}
```


### PATCH /actors/<int:actor_id>
- [Permissions] Casting Director and Executive Producer.
- [General] If the user has given a legitimate actor_id, this endpoint checks if the request body included any of name, age and gender. Whichever attributes are present are updated in the database. It returns a success message and the id of the updated actor.

```
{
  "success": true,
  "updated actor": 15
}  
```


### PATCH /movies/<int:movie_id>
- [Permissions] Casting Director and Executive Producer.
- [General] If the user has given a legitimate movie_id, this endpoint checks if the request body included either of title and release_date. Whichever attributes are present are updated in the database. It returns a success message and the id of the updated movie.

```
{
  "success": true,
  "updated movie": 2
}  
```


### DELETE /actors/<int:actor_id>/delete
- [Permissions] Casting Director and Executive Producer.
- [General] Deletes the actor with actor_id given by the user, if it exists in the database. Returns a success message, the actor id of the deleted actor and the total number of actors in our database.

```
{
  "deleted": 85,
  "success": true,
  "total actors": 90
}  
```

### DELETE /movies/<int:movie_id>/delete
- [Permissions] Executive Producer.
- [General] Deletes the movie with movie_id given by the user, if it exists in the database. Returns a success message, the movie id of the deleted movie and the total number of movies in our database.

```
{
  "deleted": 4,
  "success": true,
  "total movies": 11
}  
  
```

### POST /actors/create
- [Permissions] Casting Director and Executive Producer.
- [General] Creates a new actor in the database. If any of name, age and gender are missing, the actor will not be added to the database. Returns a success message and the name of the new actor.

```
{
  "success": true,
  "new actor": "Magnolia"
}  
```

### POST /movies/create
- [Permissions] Executive Producer.
- [General] Creates a new movie in the database. If either of title and release_date are missing, the movie will not be added to the database. Returns a success message and the title of the new movie.

```
{
  "success": true,
  "new movie": "Mi Vida"
}  
```


## Authors 
All code was written by me, Ailsa Robertson, to meet the Full Stack Nanodegree project requirements (or so I hope).


## Acknowledgements
Thanks to James Wilson for helping troubleshoot errors, and to the Udacity mentors for their contribution to the mentor help platform.  