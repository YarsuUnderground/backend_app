from flask import request , Response, g ,flash, url_for, session , redirect ,current_app , Blueprint , render_template , get_flashed_messages , jsonify
from datetime import datetime , date
from werkzeug.security import check_password_hash, generate_password_hash
from bson import json_util
from bson.objectid import ObjectId
import functools,json,os, hashlib, json
from . import database, helper
from datetime import datetime
#subtasks notification
ta = Blueprint('/tasks',__name__, url_prefix='/tasks')

def notify_executors(users_col, task_id, executors, action="$push",category="tasks"):
    if executors is None:
        return
    for executor in executors:
        users_col.update_one({'_id': executor}, {"{}".format(action):{"{}".format(category):task_id}})

def notify_on_update_tasks(users_col, task_id , executors):
    if executors is None:
        return
    users = users_col.find()
    for user in users:
        if (task_id in user['tasks']) and (user['_id'] not in executors):
            users_col.update_one({'_id': int(user['_id'])}, {"$pull":{"tasks":task_id}})
        elif (task_id not in user['tasks']) and (user['_id'] in executors):
            users_col.update_one({'_id': int(user['_id'])}, {"$push":{"tasks":task_id}})

def notify_on_update_subtasks(users_col, subtask_id, executors):
    users = users_col.find()
    for user in users:
        if (user['_id'] in executors) and (subtask_id not in user['subtasks']):
            user_col.update_one({'_id':int(user['_id'])}, {"$push":{"subtasks":subtask_id}})
        elif (user['_id'] not in executors) and (subtask_id in user['subtasks']):
            user_col.update_one({'_id':int(user['_id'])}, {"$pull":{"subtasks":subtask_id}})

@ta.route('/create/', methods=['GET', 'POST'])
def create_task():
    data = request.get_json(silent = True)
    if data is None:
        data = request.args 
    print(data)
    tasks_col = database.get_db_connection()[database.TASKS_COLLECTION_NAME]
    creator_id = data.get('creatorId') # должно быть String
    name = data.get('name')
    description = data.get('description')
    tags = data.get('tags') or []
    deadline = data.get('deadline') # to datetime.datetime?
    performers = data.get('performers') or []
    subtasks = data.get('subtasks') or []
    new_id = helper.get_next_id(tasks_col,'_id')
    task = {'_id':new_id, 'creator_id':creator_id, 'name': name, 'description':description, 'tags':tags, 'deadline': deadline, 'performers': performers, 'subtasks':subtasks }
    tasks_col.insert_one(task)
    notify_executors(database.get_db_connection()[database.USERS_COLLECTION_NAME],new_id,performers, action="$push")
    return Response(status = 200)

@ta.route('/create_subtask/', methods=['GET', 'POST',])
def create_subtask():
    data = request.get_json(silent = True)
    if data is None:
        data = request.args
    tasks_col = database.get_db_connection()[database.TASKS_COLLECTION_NAME]
    subtasks_col = database.get_db_connection()[database.SUBTASKS_COLLECTION_NAME]
    task_id = data.get('taskId')
    creator_id = data.get('creatorId') # должно быть String
    name = data.get('name')
    description = data.get('description')
    deadline = data.get('deadline') # to datetime.datetime?
    performers = data.get('performers') or []
    status = data.get('status')
    new_id = helper.get_next_id(subtasks_col,'_id')
    subtask = {'_id':new_id, 'creator_id':creator_id, 'name': name, 'description':description, 'deadline': deadline, 'performers': performers, 'status':status}
    subtasks_col.insert_one(subtask)
    tasks_col.update_one({'_id': int(task_id)}, {"$push":{"subtasks":new_id}})
    notify_executors(database.get_db_connection()[database.USERS_COLLECTION_NAME],new_id,performers, action="$push", category="subtasks")
    return Response(status = 200)

@ta.route('/delete/', methods=['GET', 'DELETE'])
def delete_task():
    data = request.get_json(silent = True)
    if data is None:
        data = request.args
    id = data.get('id')
    tasks_col = database.get_db_connection()[database.TASKS_COLLECTION_NAME]
    performers = tasks_col.find_one({'_id':id})['performers'] 
    tasks_col.delete_one({'_id':id})
    notify_executors(database.get_db_connection()[database.USERS_COLLECTION_NAME],id,performers, action="$pull")
    return Response(status = 200)

@ta.route('/delete_subtask/', methods=['GET', 'DELETE'])
def delete_subtask():
    data = request.get_json(silent = True)
    if data is None:
        data = request.args
    subtask_id = data.get('id')
    tasks_col = database.get_db_connection()[database.TASKS_COLLECTION_NAME]
    subtasks_col = database.get_db_connection()[database.SUBTASKS_COLLECTION_NAME]
    tasks_col.update({},{"$pull":{'subtasks':subtask_id}})
    subtasks_col.delete_one({'_id':int(subtask_id)})
    notify_executors(database.get_db_connection()[database.USERS_COLLECTION_NAME],subtask_id,performers, action="$pull",category="subtasks")
    return Response(status = 200)
# task_id , key, value
@ta.route('/update/', methods=['GET', 'UPDATE'])
def update_task():
    data = request.get_json(silent = True)
    if data is None:
        data = request.args
    tasks_col = database.get_db_connection()[database.TASKS_COLLECTION_NAME]
    tasks_col.update_one({'_id':int(data.get('id'))},{"$set":{'name':data.get('name'), 'description':data.get('description'), 'tags':data.get('tags'), 'deadline':data.get('deadline'), 'performers':data.get('performers'), 'subtasks':data.get('subtasks') }})
    notify_on_update_tasks(database.get_db_connection()[database.USERS_COLLECTION_NAME], data.get('id'), data.get('executors'))
    return Response(status=200)

@ta.route('/update_subtask/', methods=['GET', 'UPDATE'])
def update_subtask():
    data = request.get_json(silent = True)
    if data is None:
        data = request.args
    subtasks_col = database.get_db_connection()[database.SUBTASKS_COLLECTION_NAME]
    subtasks_col.update_one({'_id':int(data.get('id'))},{"$set":{'name':data.get('name'), 'description':data.get('description'),'deadline':data.get('deadline'), 'performers':data.get('performers'), 'status':data.get('status') }})
    notify_on_update_subtasks(database.get_db_connection()[database.USERS_COLLECTION_NAME], data.get('id'), data.get('executors'))
    return Response(status=200)   

 #-      

@ta.route('/task/', methods=['GET','POST'])
def get_task():
    data = request.get_json(silent = True)
    if data is None:
        data = request.args
    task_id = data.get('id')
    return jsonify(database.get_db_connection()[database.TASKS_COLLECTION_NAME].find_one({'_id':int(task_id)}))
    
@ta.route('/subtask/', methods=['GET','POST'])
def get_subtask():
    data = request.get_json(silent = True)
    if data is None:
        data = request.args
    subtask_id = data.get('id')
    return jsonify(database.get_db_connection()[database.SUBTASKS_COLLECTION_NAME].find_one({'_id':int(subtask_id)}))

@ta.route('/all/', methods=['GET'])
def get_all_tasks():
    tasks_col = database.get_db_connection()[database.TASKS_COLLECTION_NAME].find()
    tasks = []
    for task in tasks_col:
        tasks.append(task)
    return jsonify(tasks)  

@ta.route('/all_subtasks/', methods=['GET'])
def get_all_subtasks():
    subtasks_col = database.get_db_connection()[database.SUBTASKS_COLLECTION_NAME].find()
    subtasks = []
    for subtask in subtasks_col:
        subtasks.append(subtask)
    return jsonify(subtasks)
