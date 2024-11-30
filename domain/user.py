from datetime import datetime as dt
from mongodb.base import MongoEntity
from addict import Dict

import hashlib

class User(MongoEntity):
    
    def __init__(self, *args, **kwargs):      
                
        self.date_created: dt = None
        self.last_updated: dt = None
        self.expiration_date: dt = None
        
        self.username: str
        self.password: str
        self.name: str
        self.email: str
        self.role: str
    
        self.authorizations = []
        
        self.enabled: bool = True
        self.expired: bool = False    
        
        super().__init__(*args, **kwargs) 
                
    def to_string(self):
        return f"{self.full_name} <{self.username}>"
        