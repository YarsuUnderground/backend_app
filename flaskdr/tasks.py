from flask import request , Response, g ,flash, url_for, session , redirect ,current_app , Blueprint , render_template , get_flashed_messages , jsonify
from datetime import datetime , date
from werkzeug.security import check_password_hash, generate_password_hash
from bson import json_util
from bson.objectid import ObjectId
import functools,json,os, hashlib
from . import database
from datetime import datetime

ta = Blueprint('/tasks',__name__, url_prefix='/tasks')

@ta.route('/create/', methods=['GET', 'POST'])
def create_task():
    data = request.get_json(silent = True)
    if data is None:
        data = request.args
    #number = data.get('number')
    title = data.get('title')
    description = data.get('description')
    deadline = requests.get('deadline') # to datetime.datetime?
    executors = data.get('executors')
    tasks_col = database.get_db_connection()[database.TASKS_COLLECTION_NAME]
    #task = {}
    task = {'number': number, 'title': title, 'description':description, 'deadline': datetime.now(), 'executors': executors }
    tasks_col.insert_one(task)

@ta.route('/delete/', methods=['GET', 'DELETE'])
def delete_task():
    data = request.get_json(silent = True)
    if data is None:
        data = request.args
    id = request.get('id')
    tasks_col = database.get_db_connection()[database.TASKS_COLLECTION_NAME]
    tasks_col.delete_one({'_id':ObjectId(id)})
    return Response(status = 200)

@ta.route('/update/', methods=['GET', 'UPDATE'])
def update_task():
    pass

@ta.route('/all/', methods=['GET'])
def create_task():
    tasks_col = database.get_db_connection()[database.TASKS_COLLECTION_NAME]
    jsonify(task_col)
    #number =  