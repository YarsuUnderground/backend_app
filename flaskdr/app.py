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
    #app.register_blueprint(user.us)
    #app.register_blueprint(tasks.ta)
    #app.register_blueprint(search.se)
    #app.register_blueprint(auth.us)
    #database.init_db(app)
    #db.init_db(app) 
    @app.route('/', methods=['GET', 'POST'])
    def hello_world():
        return 'Hello, World!'

    @app.route('/db/', methods=['GET','POST'])
    def get_db():
        client = MongoClient(DATABASE_URI)
        db = client[DB_NAME]
        users_col = db['Users']
        admins_col = db['Admins']
        tasks_col = db['Tasks']
        return "Done!"
        #dcr_vo = client['DCR_VO_DATABASE']
        #col = db.listingandreviews
    """
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        if isinstance(e,InternalServerError):
            print(traceback.format_exc())
            return jsonify(error = -1 , messages = "Упс,произошла ошибка на сервере. Попробуйте выполнить действие ещё раз")
        return jsonify(error = -2 , messages = "Упс,произошла ошибка при передаче данных. Попробуйте ещё раз")
       
    @app.errorhandler(ConnectionFailure)
    def database_exception(e):
        print(traceback.format_exc())
        jsonify(error = -3 , messages = "Не удаётся выполнить запрос к базе данных. Попробуйте ещё раз")
    """
    return app