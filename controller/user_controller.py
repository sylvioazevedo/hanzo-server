from controller.base_controller import BaseController

from domain.user import User

class UserController(BaseController):
    
    def __init__(self) -> None:
        super().__init__(User)