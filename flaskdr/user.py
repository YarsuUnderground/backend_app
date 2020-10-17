from flask import request , Response, g ,flash, url_for, session , redirect ,current_app , Blueprint , render_template , get_flashed_messages , jsonify
from datetime import datetime , date
from werkzeug.security import check_password_hash, generate_password_hash
from bson import json_util
from bson.objectid import ObjectId
import functools,json,os, hashlib
from . import database 

us =  Blueprint('/user', __name__, url_prefix='/user')

@us.route('/get_type/<token>/')
def get_type(token):
    #token = request.args.get('token')
    users_col = database.get_db_connection()[database.USERS_COLLECTION_NAME]
    return jsonify('isAdmin': users_col.find_one({'token':token})['isAdmin'])

@us.route('/get_id/<token>/')
def get_id(token):
    #token = request.args.get('token')
    users_col = database.get_db_connection()[database.USERS_COLLECTION_NAME]
    return jsonify('id': users_col.find_one({'token':token})['_id'].toString())

@us.route('/get_user/<id>/')
def get_user(id):
    #id = request.args.get('id')
    users_col = database.get_db_connection()[database.USERS_COLLECTION_NAME]
    doc = users_col.find_one({'_id':id}) 
    data = {"first_name":doc['first_name'],"second_name":doc['last_name'],"isAdmin":doc['isAdmin'],"email":doc['login'],"phone":doc['phone']}
    return jsonify(data)

