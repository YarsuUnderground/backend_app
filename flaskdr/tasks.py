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
    id = data.get('id')
    creator_id = data.get('creatorId')
    name = data.get('name')
    description = data.get('description')
    tags = data.get('tags')
    deadline = requests.get('deadline') # to datetime.datetime?
    performers = data.get('performers')
    subtasks = data.get('subtasks')
    tasks_col = database.get_db_connection()[database.TASKS_COLLECTION_NAME]
    #task = {} string
    #task = {'_id':ObjectId(id), 'creator_id':ObjectId(id), 'name': name, 'description':description, 'tags':tags, 'deadline': deadline, 'performers': performers, 'subtasks':subtasks }
    task = {'_id':id, 'creator_id':creator_id, 'name': name, 'description':description, 'tags':tags, 'deadline': deadline, 'performers': performers, 'subtasks':subtasks }
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
def get_all_tasks():
    tasks_col = database.get_db_connection()[database.TASKS_COLLECTION_NAME]
    jsonify(task_col)
    #number =  