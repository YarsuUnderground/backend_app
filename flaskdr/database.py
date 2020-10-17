from pymongo import MongoClient
from flask import current_app , g
COLLECTION_NAME = "Users"
USERS_COLLECTION_NAME = "Users"
ADMINS_COLLECTION_NAME = "Admins"
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
