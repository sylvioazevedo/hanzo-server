from controller.secure_base_controller import SecureBaseController
from domain.role import Role

class RoleController(SecureBaseController):
    
    def __init__(self) -> None:
        super().__init__(Role)
        
