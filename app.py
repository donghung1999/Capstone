from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import Actors, Movies, setup_db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
      response.headers.add('Access-Control-Allow-Headers',
                            "Content-Tpe,Authorization,true")
      response.headers.add('Access-Control-Allow-Methods',
                            'GET,PUT,POST,PATCH,DELETE,OPTIONS')
      return response
  
    @app.route('/movies', methods = ['GET'])
    @requires_auth('get:all-movies-detail')
    def GetMoviesObjectInDatabase(getInputPayload):
        return jsonify({
            "success": True, 
            "movies": [item.format() for item in Movies.query.filter(Movies.is_delete == False).all()]
        })

    @app.route('/movies', methods = ['POST'])
    @requires_auth('create:new-movies-detail')
    def CreateMoviesObjectInDatabase(getInputPayload):
        if not ('title' in request.get_json() and 'release_date' in request.get_json()):
            abort(400)
        try:
            createMoviesObject = Movies()
            createMoviesObject.title = request.get_json().get('title', None)
            createMoviesObject.release_date = request.get_json().get('release_date', None)
            createMoviesObject.insert()
        except Exception as e:
            abort(500)

        return jsonify({
            "success": True, 
            "movies": [createMoviesObject.format()]
        })

    @app.route('/movies/<id>', methods = ['PATCH'])
    @requires_auth('patch:exist-movies-detail')
    def UpdateMoviesObjectInDatabase(getInputPayload, id):
        if not ('title' in request.get_json() and 'release_date' in request.get_json()):
            abort(400)
        getMoviesDataFromDb = Movies.query.filter(Movies.is_delete == False).filter(Movies.id == id).first()
        if not getMoviesDataFromDb:
            abort(404)
        try:
            getMoviesDataFromDb.title = request.get_json().get('title', None)
            getMoviesDataFromDb.release_date = request.get_json().get('release_date', None)
            getMoviesDataFromDb.update()
        except Exception as e:
            abort(500)

        return jsonify({
            "success": True, 
            "movies": [getMoviesDataFromDb.format()]
        })
    
    @app.route('/movies/<id>', methods = ['DELETE'])
    @requires_auth('delete:exist-movies-detail')
    def DeleteMoviesObjectInDatabase(getInputPayload, id):
        getMoviesDataFromDb = Movies.query.filter(Movies.is_delete == False).filter(Movies.id == id).first()
        if not getMoviesDataFromDb:
            abort(404)
        try:
            getMoviesDataFromDb.delete()
        except Exception as e:
            abort(500)

        return jsonify({
            "success": True, 
            "delete": id
        })

  # Actors Api

    @app.route('/actors', methods = ['GET'])
    @requires_auth('get:all-actors-detail')
    def GetActorsObjectInDatabase(getInputPayload):
        return jsonify({
            "success": True, 
            "actors": [item.format() for item in Actors.query.filter(Actors.is_delete == False).all()]
        })

    @app.route('/actors', methods = ['POST'])
    @requires_auth('post:new-actors-detail')
    def CreateActorsObjectInDatabase(getInputPayload):
        if not ('name' in request.get_json() and 'age' in request.get_json() and 'gender' in request.get_json()):
            abort(400)
        try:
            createActorsObject = Actors()
            createActorsObject.name = request.get_json().get('name', None)
            createActorsObject.age = request.get_json().get('age', None)
            createActorsObject.gender = request.get_json().get('gender', None)
            createActorsObject.insert()
        except Exception as e:
            abort(500)

        return jsonify({
            "success": True, 
            "actors": [createActorsObject.format()]
        })

    @app.route('/actors/<id>', methods = ['PATCH'])
    @requires_auth('patch:exist-actors-detail')
    def UpdateActorsObjectInDatabase(getInputPayload, id):
        if not ('name' in request.get_json() and 'age' in request.get_json() and 'gender' in request.get_json()):
            abort(400)
        getActorsDataFromDb = Actors.query.filter(Actors.is_delete == False).filter(Actors.id == id).first()
        if not getActorsDataFromDb:
            abort(404)
        try:
            getActorsDataFromDb.name = request.get_json().get('name', None)
            getActorsDataFromDb.age = request.get_json().get('age', None)
            getActorsDataFromDb.gender = request.get_json().get('gender', None)
            getActorsDataFromDb.update()
        except Exception as e:
            abort(500)

        return jsonify({
            "success": True, 
            "actors": [getActorsDataFromDb.format()]
        })

    @app.route('/actors/<id>', methods = ['DELETE'])
    @requires_auth('delete:exist-actors-detail')
    def DeleteActorsObjectInDatabase(getInputPayload, id):
        getActorsDataFromDb = Actors.query.filter(Actors.is_delete == False).filter(Actors.id == id).first()
        if not getActorsDataFromDb:
            abort(404)
        try:
            getActorsDataFromDb.delete()
        except Exception as e:
            abort(500)

        return jsonify({
            "success": True, 
            "delete": id
        })
  
    @app.errorhandler(400)
    def BadRequestFromClient(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400
  
    @app.errorhandler(404)
    def NotFoundFromClient(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Requested Page Is Not Available"
        }), 404
    
    @app.errorhandler(500)
    def InternalServerErrorFromClient(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500
    
    @app.errorhandler(AuthError)
    def ReturnAuthError(getInputError):
        return jsonify({
            "success": False,
            "error": getInputError.status_code,
            "message": getInputError.error['description']
        }), getInputError.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run()