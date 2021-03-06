from flask import Flask , request , render_template , Response , jsonify , session
from flask_cors import CORS
from pymongo.errors import ConnectionFailure
from werkzeug.exceptions import HTTPException, InternalServerError
from flask_cors import CORS
from pymongo import MongoClient
from . import auth, database, search, user, tasks
SECRET_KEY = "*F-JaNdRgUkXp2s5v8y/B?E(H+KbPeSh"
CONNECTION_PASSWORD_PROJECT_2="UJPzENtW2usNKzUj"
DATABASE_USER = "db_admin"
DB_USER_CONNECTION_PASSWORD = "Bs9YihdUQSv4dCJ"
DB_NAME = "DCR_VO_DATABASE"
DATABASE_URI = "mongodb+srv://{}:{}@cluster1.8eqkp.mongodb.net/{}?retryWrites=true&w=majority".format(DATABASE_USER, DB_USER_CONNECTION_PASSWORD, DB_NAME)
def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
            SECRET_KEY= SECRET_KEY,
            DATABASE_URI = DATABASE_URI,
            DB_NAME = DB_NAME
        )
    CORS(app, supports_credentials = True)
    app.register_blueprint(auth.bp)
    app.register_blueprint(user.us)
    app.register_blueprint(tasks.ta)
    app.register_blueprint(search.se)
    #database.init_db(app)
    #db.init_db(app) 
    @app.route('/', methods=['GET', 'POST'])
    def hello_world():
        return 'Hello, World!'
    """
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        if isinstance(e,InternalServerError):
            return Response(status=500)
        return Response(status=500)
       
    @app.errorhandler(ConnectionFailure)
    def database_exception(e):
        print(traceback.format_exc())
        return Response(status_code=500)
    """
    return app