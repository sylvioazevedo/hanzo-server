from addict import Dict
from bson import json_util
from domain.role import Role
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from flaskr.auth import role_required

class SecureBaseController():
    
    def __init__(self, _class) -> None:        
        
        self._class = _class
        self._route = _class.__name__.lower()
        self._path = f"{_class.__module__}.{_class.__name__}"
    
        self.bp = Blueprint(self._route, self._class.__module__, url_prefix=f"/{self._route}")
        
        @self.bp.route("/", methods=["GET"])
        @jwt_required()
        @role_required('admin')
        def list():
            return json_util.dumps([o.__dict__ for o in self._class.list()])
        
        # find all by query, sort, order, limit, skip, projection and GET method
        @self.bp.route("/find", methods=["GET"])
        @jwt_required()
        @role_required('admin')
        def find_all_by():
            query = Dict(request.args)
            sort = query.pop('sort', None)
            order = query.pop('order', None)
            limit = query.pop('max', None)
            limit = int(limit) if limit else None
            skip = query.pop('page', None)
            skip = int(skip) if skip else None
            projection = query.pop('projection', None)
            
            return json_util.dumps([o.__dict__ for o in self._class.find_all_by(query, sort, order, limit, skip, projection)])
        
        @self.bp.route("/count", methods=["GET"])
        @jwt_required()
        def count():
            query = Dict(request.args)            
            return json_util.dumps(self._class.count(query))        
        
        @self.bp.route("/<id>", methods=["GET"])
        @jwt_required()
        @role_required('admin')
        def get(id):
            return json_util.dumps(self._class.find_by_id(id).__dict__)
        
        @self.bp.route("/<id>", methods=["DELETE"])
        @jwt_required()
        @role_required('admin')
        def delete(id):
            
            obj = self._class.find_by_id(id)
            
            if not obj:
                return "Not found", 404            
                  
            return json_util.dumps(obj.delete())
        
        @self.bp.route("/", methods=["POST"])
        @jwt_required()
        @role_required('admin')
        def insert():
            
            # Get data from incoming request JSON
            data = request.get_json()
            
            if not data:
                return "No data received", 400                     
            
            return json_util.dumps(self._class(data).save())
        
        
        @self.bp.route("/", methods=["PUT"])
        @jwt_required()
        @role_required('admin')
        def update():
            
            # Get data from incoming request JSON
            data = Dict(request.get_json())
            
            if not data:
                return "No data received", 400     
            
            obj = self._class.find_by_id(data._id)
            
            del(data['_id'])                        
                
            r = obj.update(data)
                             
            return json_util.dumps(r.raw_result)
        
        
        