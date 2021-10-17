from sanic import Sanic
from sanic_ext import Extend
from tortoise.contrib.sanic import register_tortoise

from user_api import logger
from user_api.database import DatabaseProvider
from user_api.routes import blueprint
from user_api.settings import config

app = Sanic("User API")
app.config.update(config.dict())
app.config.FALLBACK_ERROR_FORMAT = "json"
Extend(app)
app.blueprint(blueprint)

logger.setup_logger(app)
logger.log_middleware_setup(app)


db_config = DatabaseProvider(
    "user_api",
    apps=["auth", "users"],
    sanic=app,
    aerich=True,
).register(config.database_uri, False)
