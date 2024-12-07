from dataclasses import dataclass, field
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
    role: str = field(default=None, metadata='list: ["admin", "user"]')	
    
    authorizations = []
        
    enabled: bool = True
    expired: bool = False

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
                
    def to_string(self):
        return f"{self.name} <{self.username}>"
        