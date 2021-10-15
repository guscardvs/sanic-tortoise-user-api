from sanic import Sanic
from sanic_ext import Extend
from tortoise.contrib.sanic import register_tortoise

from user_api.routes import blueprint
from user_api.settings import config

app = Sanic("User API")
app.config.update(config.dict())
app.config.FALLBACK_ERROR_FORMAT = "json"
Extend(app)
app.blueprint(blueprint)

register_tortoise(
    app,
    db_url="sqlite://:memory:",
    modules={"models": ["user_api.users.models", "user_api.auth.models"]},
    generate_schemas=True,
)
