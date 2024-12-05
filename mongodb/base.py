
from addict import Dict
from bson.objectid import ObjectId
from datetime import datetime as dt
from mongodb.connection import get_db
from werkzeug.security import generate_password_hash

class MongoEntity(Dict):
    
    _db = None
    
    def __init__(self, *args, **kwargs):
        
        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        
        for key in kwargs:
            setattr(self, key, kwargs[key])     
                              
    @classmethod        
    def get_collection(cls):             
        MongoEntity._db = get_db() if MongoEntity._db is None else MongoEntity._db      
        return MongoEntity._db[cls.__name__.lower()]
    
    @classmethod
    def get_collection_name(cls):
        return cls.__name__.lower() 
        
    @classmethod  
    def list(cls):    
        return [cls(i) for i in cls.get_collection().find()]
    
    @classmethod
    def find_by_id(cls, id):
        _doc = cls.get_collection().find_one({"_id": ObjectId(id)})
        _doc['_id'] = str(_doc['_id'])
        return cls(_doc) if _doc else None 
    
    @classmethod
    def find_by(cls, _query):        
        _doc = cls.get_collection().find_one(_query)
        
        if not _doc:
            return None
        
        _doc['_id'] = str(_doc['_id'])
        
        return cls(_doc)
    
    @classmethod
    def find_all_by(cls, _query, sort=None, order=None, limit=None, skip=None, projection=None):   

        # todo: change skip limit to sequence number find limit to improve performance. 

        if sort:
            _sort = [(sort, int(order))]
            return [cls(i) for i in cls.get_collection().find(_query, projection, skip=limit*(skip-1), limit=limit).sort(_sort)]
        else:
            _sort = None        
            return [cls(i) for i in cls.get_collection().find(_query, projection, skip=limit*(skip-1), limit=limit)]
    
    @classmethod
    def count(cls, _query):
        return cls.get_collection().estimated_document_count(_query)
    
    # instance methods
    #    
    def add_to_set(self, prop, value):
        return self.get_collection().update_one({"_id": ObjectId(self._id)}, {"$addToSet": {prop: value}})
    
    def remove_from_set(self, prop, value):
        return self.get_collection().update_one({"_id": ObjectId(self._id)}, {"$pull": {prop: value}})
    
    def update(self, data):
        
        if 'last_updated' in self:
            self.last_updated = dt.now()

        if 'password' in data and data.password:
            data.password = self._set_password(data.password)
        else:
            del(data['password'])
        
        return self.get_collection().update_one({"_id": ObjectId(self._id)}, {'$set': data})    
    
    def save(self):
        
        if 'date_created' in self.keys():
            self.date_created = dt.now()
            
        if 'last_updated' in self.keys():
            self.last_updated = dt.now()

        if 'password' in self.keys():
            self.password = self._set_password(self.password)
        
        _o = self.get_collection().insert_one(self)
        self._id = _o.inserted_id
        
        return {"id": str(self._id)}
        
    def delete(self):
        r = self.get_collection().delete_one({"_id": ObjectId(self._id)})
        
    
    def _set_password(self, password):        
        return generate_password_hash(password)
    