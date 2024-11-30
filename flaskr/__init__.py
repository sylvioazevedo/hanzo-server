from controller.role_controller import RoleController
from controller.user_controller import UserController

from datetime import datetime as dt
from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import JWTManager, get_jwt_identity
from instance.config import SERVER_FULL_NAME, SERVER_PORT, JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES, JWT_REFRESH_TOKEN_EXPIRES

from . import auth
from . import db

import os

def shutdown_server():
    '''
    Shutdown Flask Application server
    '''
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if shutdown is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    
    shutdown()

def create_app(test_config=None):
    '''
    Create and configure the Flask Application
    '''
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # configure JWT engine
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = JWT_REFRESH_TOKEN_EXPIRES
    jwt = JWTManager(app)

    # print server configuration
    print(f'Running {SERVER_FULL_NAME} on port {SERVER_PORT}...')
    print(f'Configuration:')
    print(f'{app.config}')
    print('--')    

    # register cli commands
    db.init_app(app)

    # register blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(RoleController().bp)
    app.register_blueprint(UserController().bp)

    # server info
    @app.route('/')
    def index():
        return jsonify({
            'server': SERVER_FULL_NAME,
            'datetime': dt.now().isoformat()
        })
    
    # server jwt session info
    @app.route('/session')
    def session():
        return jsonify(f'{get_jwt_identity()}')
    
    # ping
    @app.route('/ping')
    def ping():
        return jsonify({
            'msg': 'pong',
            'timestamp': dt.now().isoformat()
        })
    
    # shutdown
    @app.route('/shutdown', methods=['POST'])
    def shutdown():
        shutdown_server()
        return jsonify({
            'msg': 'shutting down server',
            'timestamp': dt.now().isoformat()
        })
    
    return app
