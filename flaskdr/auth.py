from flask import request , g ,flash, url_for, session , redirect ,current_app , Blueprint , render_template , get_flashed_messages , jsonify
from datetime import datetime , date
from werkzeug.security import check_password_hash, generate_password_hash
from bson import json_util
import functools,json,os
from . import database 
#from flaskdr.user import User 

bp = Blueprint('/auth', __name__, url_prefix='/auth')

@bp.route('/register/', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return "GET-method" + url_for('register')
    else:
        return "POST_method" + url_for('register')

@bp.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return "GET-method" + url_for('register')
    else:
        return "POST_method" + url_for('register')

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