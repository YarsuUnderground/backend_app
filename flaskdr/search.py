from flask import request , Response, g ,flash, url_for, session , redirect ,current_app , Blueprint , render_template , get_flashed_messages , jsonify
from datetime import datetime , date
from werkzeug.security import check_password_hash, generate_password_hash
from bson import json_util
from bson.objectid import ObjectId
import functools,json,os, hashlib
from . import database 

se = Blueprint('/search', __name__, url_prefix='/search/')

@se.route('/tasks/', methods = ['GET', 'POST'])
def get_dialogue():
    data = request.get_json(silent = True)
    if data is None:
        data = request.args
    tags = data.get('tags')
    tasks_col = database.get_db_connection()[database.TASKS_COLLECTION_NAME] 
    tasks = []
    #tasks = tasks_col.find({'tags': {"$in": tags}}) - вдруг сработает
    for cursor in tasks_col.find({}):
        for tag in cursor['tags']:
            if tag in tags:
                tasks.append(cursor)
                continue
    return jsonify(tasks)