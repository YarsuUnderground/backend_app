from flask import request , Response, g ,flash, url_for, session , redirect ,current_app , Blueprint , render_template , get_flashed_messages , jsonify
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
    data = request.get_json(silent = True)
    if data is None:
        print("Register failed: couldn't parse to json")
        return Response(status=400)
    first_name = data.get('first_name')
    last_name = data.get('second_name')
    login = data.get('email') #email
    users_col = database.get_db_connection()[database.USERS_COLLECTION_NAME]#DATABASE = DCR_VO_DATABASE
    if users_col.find_one({"login":login}) is not None:
        return Response(status=401)
    password = data.get('password')
    phone = data.get('phone')
    token = hashlib.md5((first_name + last_name + login).encode() + os.urandom(16)).hexdigest()
    user = {'login': login,'first_name':first_name, 'second_name':last_name, 'password':generate_password_hash(password), 'phone': phone}
    users_col.insert_one(user)
    data = {'token':token}
    return jsonify(data)

@bp.route('/register_admin', methods=['POST'])
def register_admin():
    pass

@bp.route('/login/', methods=['POST'])
def login_users():
    data = request.get_json(silent = True)
    login = data.get('login')
    password = data.get('password')
    users_col = database.get_db_connection()[database.USERS_COLLECTION_NAME]#DATABASE = DCR_VO_DATABASE
    user = users_col.find_one({"login":login})
    if user is None:
        return Response(status=401)
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
        return  jsonify(credentials = credentials)
    else:
        return Response(status=401)

@bp.route('/login_admin/', methods=['POST'])
def login_admin():
    data = request.json(force = True)
    login = data.get('login')
    password = data.get('password')
    code = 200
    users_col = database.get_db_connection()[database.USERS_COLLECTION_NAME]#DATABASE = DCR_VO_DATABASE
    user = users_col.find_one({"login":login})
    return "admin"

@bp.route('/logout/', methods=['GET' ,'POST'])
def logout():
    #print("From logout() - The user is: " + str(session.get("user")))
    session.clear()
    return Response(status=200)

"""
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
"""

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            error = 3
            return jsonify( error = error, message = "Необходима авторизация")
        return view(**kwargs)
    return wrapped_view