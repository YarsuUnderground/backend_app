from flask import request , g ,flash, url_for, session , redirect ,current_app , Blueprint , render_template , get_flashed_messages , jsonify
from datetime import datetime , date
from werkzeug.security import check_password_hash, generate_password_hash
from bson import json_util
import functools,json,os, hashlib
from . import database 
#from flaskdr.user import User 
# добавить проверки!
# сессии!
bp = Blueprint('/auth', __name__, url_prefix='/auth')

@bp.route('/register/', methods=['POST'])
def register():
    data = request.json(silent = True)
    if data is None:
        print("Register failed: couldn't parse to json")
        return jsonify(code=-1, messages="Couldn't parse to json")
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    login = data.get('login') #email
    users_col = database.get_db_connection()[database.USERS_COLLECTION_NAME]#DATABASE = DCR_VO_DATABASE
    if users_col.find_one({"login":login}) is not None:
        return jsonify(code=-2, messages="User with same login already exists")
    password = data.get('password')
    phone = data.get('phone')
    token = (first_name + last_name + login).encode() + os.urandom(16)
    user = {'login': login,'first_name':first_name, 'last_name':last_name, 'password':generate_password_hash(password), 'phone': phone}
    users_col.insert_one(user)
    return jsonify(code = 200, token = token)

@bp.route('/register_admin', methods=['POST'])
def register_admin():
    pass


@bp.route('/login/', methods=['POST'])
def login_users():
    data = request.json(silent = True)
    login = data.get('login')
    password = data.get('password')
    code = 200
    users_col = database.get_db_connection()[database.USERS_COLLECTION_NAME]#DATABASE = DCR_VO_DATABASE
    user = users_col.find_one({"login":login})
    if user is None:
        error = -1
        flash("Не существует пользователя с таким логином")
    elif check_password_hash(user['password'],password):
        #session.clear()
        ##session.pop("user",None)
        #session.pop("user_id",None)
        ##session['user'] = user.get_user_data_no_passwd()
        ##print("From login() - The user is:"+ str(session.get("user")))
        #session['user_id'] = str(doc['_id'])
        first_name, last_name = user['first_name'] , user['last_name']
        token = (first_name + last_name + login).encode() + os.urandom(16) 
        credentials = {'token':hashlib.md5(token).hexdigest(), 'first_name': first_name, 'last_name': last_name}
        return  jsonify( code = code, credentials = credentials)
    else:
        code = -2
        flash("Неверный пароль")
    return jsonify(code = code, messages=get_flashed_messages())

@bp.route('/login_admin/', methods=['POST'])
def login_admin():
    data = request.json(force = True)
    login = data.get('login')
    password = data.get('password')
    code = 200
    users_col = database.get_db_connection()[database.USERS_COLLECTION_NAME]#DATABASE = DCR_VO_DATABASE
    user = users_col.find_one({"login":login})


@bp.route('/logout/', methods=['GET' ,'POST'])
def logout():
    #print("From logout() - The user is: " + str(session.get("user")))
    session.clear()
    return jsonify(error = 0, messages = "Пользователь вышел из аккаунта")


@bp.before_app_request
def initalize_logged_user():
    user = session.get('user')
    if user is None:
        g.user = None
        print("From initalize_logged_user() - the user is unauthorized!: ")
    else:
        print("From initalize_logged_user() - the user is authorized!: " + str(user))
        g.user = user
        #g.user_id = session.get('user_id')
        #g.user_email = session.get('user').get('email)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            error = 3
            return jsonify( error = error, message = "Необходима авторизация")
        return view(**kwargs)
    return wrapped_view