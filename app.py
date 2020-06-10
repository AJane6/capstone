import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import Actor, Movie, setup_db

RESULTS_PER_PAGE = 12


def pagination_function(request, selection):
    result = request.args.get('page', 1, type=int)
    start = (result - 1) * RESULTS_PER_PAGE
    end = start + RESULTS_PER_PAGE
    results = [result.format() for result in selection]
    current_results = results[start:end]
    return current_results


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE,OPTIONS")
        return response

    @app.route('/', methods=['GET'])
    def simple_function():
        return jsonify("Hello world")

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actor')
    def get_actors(token):
        selection = Actor.query.all()
        paginated_actors = pagination_function(request, selection)
        if len(paginated_actors) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'actors': paginated_actors,
            'total_actors': len(selection)
        })

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movie')
    def get_movies(token):
        selection = Movie.query.all()
        paginated_movies = pagination_function(request, selection)
        if len(paginated_movies) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'movies': paginated_movies,
            'total_movies': len(paginated_movies)
        })

    @app.route('/actors/create', methods=['POST'])
    @requires_auth('post:actor')
    def create_actor_submission(token):
        body = request.get_json()
        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')
        new_actor = Actor(name=name, age=age, gender=gender)
        if name is None:
            abort(422)
        if age is None:
            abort(422)
        if gender is None:
            abort(422)
        new_actor.insert()
        return jsonify({
            'success': True,
            'new actor': new_actor.name
        })

    @app.route('/movies/create', methods=['POST'])
    @requires_auth('post:movie')
    def create_movie_submission(token):
        body = request.get_json()
        title = body.get('title')
        release_date = body.get('release_date')
        new_movie = Movie(title=title, release_date=release_date)
        if title is None:
            abort(422)
        if release_date is None:
            abort(422)
        new_movie.insert()
        return jsonify({
            'success': True,
            'new movie': new_movie.title
        })

    @app.route("/actors/<int:actor_id>", methods=["PATCH"])
    @requires_auth('patch:actor')
    def update_actor(token, actor_id):
        try:
            actor = Actor.query.get(actor_id)
            if not actor:
                abort(404)
            body = request.get_json()
            updated_name = body.get('name')
            updated_age = body.get('age')
            updated_gender = body.get('gender')
            if updated_name:
                actor.name = updated_name
            if updated_age:
                actor.age = updated_age
            if updated_gender:
                actor.gender = updated_gender
            actor.update()
            return jsonify({
                'success': True,
                'updated actor': actor.id
            })
        except:
            abort(400)

    @app.route("/movies/<int:movie_id>", methods=["PATCH"])
    @requires_auth('patch:movie')
    def update_movie(token, movie_id):
        try:
            movie = Movie.query.get(movie_id)
            if not movie:
                abort(404)
            body = request.get_json()
            updated_title = body.get('title')
            updated_release_date = body.get('release_date')
            if updated_title:
                movie.title = updated_title
            if updated_release_date:
                movie.release_date = updated_release_date
            movie.update()
            return jsonify({
                'success': True,
                'updated movie': movie.id
            })
        except:
            abort(400)

    @app.route('/actors/<int:actor_id>/delete', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(token, actor_id):
        try:
            actor = Actor.query.filter_by(id=actor_id).one_or_none()
            if actor is None:
                abort(404)
            actor.delete()
            selection = Actor.query.all()
            return jsonify({
                'success': True,
                'deleted': actor_id,
                'total actors': len(selection)
            })
        except:
            abort(404)

    @app.route('/movies/<int:movie_id>/delete', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(token, movie_id):
        try:
            movie = Movie.query.filter_by(id=movie_id).one_or_none()
            if movie is None:
                abort(404)
            movie.delete()
            selection = Movie.query.all()
            return jsonify({
                'success': True,
                'deleted': movie_id,
                'total movies': len(selection)
            })
        except:
            abort(404)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(401)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable entity"
        }), 422

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(AuthError)
    def authentication_error(ex):
        return jsonify({
            "success": False,
            "error": ex.status_code,
            "message": ex.error['code']
        }), ex.status_code

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
