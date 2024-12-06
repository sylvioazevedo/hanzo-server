from bson import json_util
from controller.secure_base_controller import SecureBaseController
from flaskr.auth import role_required
from flask_jwt_extended import jwt_required
from domain.user import User

class UserController(SecureBaseController):
    
    def __init__(self) -> None:
        super().__init__(User)

        @self.bp.route("/info/<string:username>", methods=["GET"])
        @jwt_required()        
        def get_info(username):
            return json_util.dumps(self._class.find_by({'username': username}).__dict__)
