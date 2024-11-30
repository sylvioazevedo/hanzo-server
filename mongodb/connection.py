from flask import current_app, g
import pymongo as mongo

def get_db(database_name: str = None):
    '''
    Get the database connection
    '''

    print(f'Mongo_uri: {current_app.config['MONGO_URI']}')	

    if 'conn' not in g:
        g.conn = mongo.MongoClient(current_app.config['MONGO_URI'])
        
    db_name = database_name if database_name else current_app.config['MONGODB_DATABASE']
    
    return g.conn[db_name]

def close_db(e=None):
    '''
    Close the database connection
    '''
    conn = g.pop('conn', None)
    
    if conn is not None:
        conn = None

