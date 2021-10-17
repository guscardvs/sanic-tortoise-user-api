from sanic import Sanic
from sanic_ext import Extend
from tortoise.contrib.sanic import register_tortoise

from user_api import logger
from user_api.routes import blueprint
from user_api.settings import config

app = Sanic("User API")
app.config.update(config.dict())
app.config.FALLBACK_ERROR_FORMAT = "json"
app.config.API_SECURITY_DEFINITIONS = {
    "OAuth2": {
        "type": "oauth2",
        "flow": "password",
        "tokenUrl": "/auth/token",
    }
}
Extend(app)
app.blueprint(blueprint)

logger.setup_logger(app)
logger.log_middleware_setup(app)


register_tortoise(
    app,
    db_url="sqlite://:memory:",
    modules={"models": ["user_api.users.models", "user_api.auth.models"]},
    generate_schemas=True,
)
