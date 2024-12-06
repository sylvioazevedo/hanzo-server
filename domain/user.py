from dataclasses import dataclass
from datetime import datetime as dt
from mongodb.base import MongoEntity

@dataclass
class User(MongoEntity):

    date_created: dt = None
    last_updated: dt = None
    expiration_date: dt = None
        
    username: str = None
    password: str = None
    name: str = None
    email: str = None
    role: str = None
    
    authorizations = []
        
    enabled: bool = True
    expired: bool = False

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
                
    def to_string(self):
        return f"{self.full_name} <{self.username}>"
        