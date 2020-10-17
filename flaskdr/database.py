from pymongo import MongoClient
from flask import current_app , g
COLLECTION_NAME = "Users"
USERS_COLLECTION_NAME = "Users"
ADMINS_COLLECTION_NAME = "Admins"
IMAGES_COLLECTION_NAME = "Images"
TASKS_COLLECTION_NAME = "Tasks"
DATABASE = "DCR_VO_DATABASE"
ATTEMPTS = 3

def get_db_connection(database = DATABASE):
    if 'con' not in g:
        g.con = MongoClient(current_app.config['DATABASE_URI'])
        g.db = MongoClient(current_app.config['DATABASE_URI'])[database]
    return g.db

def get_col(database = DATABASE):
    if 'db' not in g:
        g.db = MongoClient(current_app.config['DATABASE_URI'])[database]
    return g.db[COLLECTION_NAME]

def get_definite_col(con_URI = None ,database = DATABASE , col_name = COLLECTION_NAME):
    if con_URI is None:
        con_URI = current_app.config[database] 
    return MongoClient(con_URI)[database][col_name]
    
def close_db_connetion(e = None):
    g.pop('db',None)
    con = g.pop('con',None)
    if con is not None:
        con.close()

def init_db(app):
    app.teardown_appcontext(close_db_connetion)
    pass


"""
User Entity:
{
'_id': ObjectId("fwefrejgoejroigre"),
'login':'login@mail.ru',
'password':'some_password',
'first_name':'Some name',
'last_name': 'Surname',
'phone':'phone_number',
'is_admin': 'False',
'token': '32frit483ut88t4u89tg8'
'tasks': '['task_id1', 'task_id2', 'task_id3']
}

Admin Entity:
{
'_id': ObjectId("fwefrejgoejroigre"),
'login':'login@mail.ru',
'password':'some_password',
'first_name':'Some name',
'last_name': 'Surname',
'phone':'phone_number',
'is_admin': 'True',
'token': '32frit483ut88t4u89tg8'
'tasks': '['task_id1', 'task_id2', 'task_id3']
}

Task Entity:
{
'_id':ObjectId('fwiorjgnregiuerge'),
'number': 1233443,
'title':'task1',
'description': 'fregerhbtrhbtrhtrhrt',
'deadline': Object(datetime.datetime)
'executers': ['user_id1', 'user_id2', 'user_id3'] # or 'login'
}

Image Entity:
{
'_id':ObjectId('fwiorjgnregiuerge'),
'user_id':'user_id', # or 'login'
'img': raw_object
}

"""