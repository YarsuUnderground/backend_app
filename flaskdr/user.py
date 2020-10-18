from flask import request , Response, g ,flash, url_for, session , redirect ,current_app , Blueprint , render_template , get_flashed_messages , jsonify
from datetime import datetime , date
from werkzeug.security import check_password_hash, generate_password_hash
from bson import json_util
from bson.objectid import ObjectId
import functools,json,os, hashlib
from . import database, helper

us =  Blueprint('/user', __name__, url_prefix='/user')

@us.route('/user_type/', methods=['GET', 'POST'])
def get_type():
    token = request.args.get('token')
    users_col = database.get_db_connection()[database.USERS_COLLECTION_NAME]
    return jsonify({'isAdmin': users_col.find_one({'token':token})['isAdmin']})

@us.route('/user_id/', methods=['GET', 'POST'])
def get_id():
    token = request.args.get('token')
    users_col = database.get_db_connection()[database.USERS_COLLECTION_NAME]
    return jsonify({'id': users_col.find_one({'token':token})['_id']})

#-
@us.route('/user_data/', methods=['GET', 'POST'])
def get_user():
    user_id = request.args.get('id')
    users_col = database.get_db_connection()[database.USERS_COLLECTION_NAME]
    doc = users_col.find_one({'_id': int(user_id)})
    if doc is None:
        return  
    data = {"first_name":doc['first_name'],"second_name":doc['last_name'],"isAdmin":doc['isAdmin'],"email":doc['login'],"phone":doc['phone']}
    return jsonify(data)

@us.route('/user_tasks/', methods=['GET', 'POST'])
def get_user_tasks():
    user_id = int(request.args.get('id'))
    users_col = database.get_db_connection()[database.USERS_COLLECTION_NAME]
    tasks = []
    documents = database.get_db_connection()[database.TASKS_COLLECTION_NAME].find()
    for cursor in documents:
        if user_id in cursor['performers']:
            tasks.append(cursor)
    return jsonify(tasks)

@us.route('/user_subtasks/', methods=['GET', 'POST'])
def get_user_subtasks():
    user_id = request.args.get('id')
    users_col = database.get_db_connection()[database.USERS_COLLECTION_NAME]
    subtasks = []
    documents = database.get_db_connection()[database.SUBTASKS_COLLECTION_NAME].find()
    for cursor in documents:
        if user_id in cursor['performers']:
            tasks.append(cursor)
    return jsonify(subtasks)


