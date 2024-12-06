from dataclasses import dataclass
from mongodb.base import MongoEntity

@dataclass
class Role(MongoEntity):

    # properties
    authority: str
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        