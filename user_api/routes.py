from sanic import Blueprint
from sanic.blueprint_group import BlueprintGroup

from user_api.auth.routes import bp as auth_bp
from user_api.users.routes import bp as user_bp
from user_api.utils.exception_handler import ExceptionHandler

blueprint = Blueprint.group(user_bp, auth_bp)  # type: BlueprintGroup

exception_handler = ExceptionHandler(blueprint)
exception_handler.setup()
