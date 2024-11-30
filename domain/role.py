from mongodb.base import MongoEntity

class Role(MongoEntity):
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        # properties
        self.authority: str