from controller.base_controller import BaseController
from domain.role import Role

class RoleController(BaseController):
    
    def __init__(self) -> None:
        super().__init__(Role)
        
