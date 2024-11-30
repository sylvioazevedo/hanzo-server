from bson import ObjectId
from datetime import datetime as dt
from flask import current_app, jsonify, request, Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from functools import wraps
from pymongo.results import InsertOneResult
from werkzeug.security import check_password_hash, generate_password_hash

from domain.user import User

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    '''
    Login endpoint
    '''
    data = request.get_json()        
    
    if not data:
        return jsonify({'msg': 'Missing JSON data'}), 400
    
    user = User.find_by({'username': data['username']})
    
    if not user:
        return jsonify({'msg': 'User not found'}), 404
        

    print(user.password)
    
    if not check_password_hash(user.password, data['password']):
        return jsonify({'msg': 'Invalid password'}), 401
    
    claims = {
        'username': user.username,
        'full_name': user.name,	
        'role': user.role
    }
    
    access_token = create_access_token(identity=user.username)
    refresh_token = create_refresh_token(identity=user.username)
    
    return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200

@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    '''
    Refresh endpoint
    '''
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    
    return jsonify({'access_token': access_token}), 200

def role_required(*required_roles):
    '''
    Role required decorator
    '''
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt_identity()
            
            if claims['role'] not in required_roles:
                return jsonify({'msg': 'Insufficient permissions'}), 403
            
            return fn(*args, **kwargs)
        return decorator
    return wrapper