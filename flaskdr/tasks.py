from flask import request , Response, g ,flash, url_for, session , redirect ,current_app , Blueprint , render_template , get_flashed_messages , jsonify
from datetime import datetime , date
from werkzeug.security import check_password_hash, generate_password_hash
from bson import json_util
from bson.objectid import ObjectId
import functools,json,os, hashlib
from . import database

ta = Blueprint('/tasks',__name__, url_prefix='/tasks')

@ta.route('/create/', methods=['GET', 'POST'])
def create_task():
    data = request.get_json(silent = True)
    #number = data.get('number')
    title = data.get('title')


@ta.route('/delete/', methods=['DELETE'])
def delete_task():
    pass

@ta.route('/update/', methods=['UPDATE'])
def update_task():
    pass

@ta.route('/all/', methods=['GET'])
def create_task():
    data = request.get_json(silent = True)
    #number =  