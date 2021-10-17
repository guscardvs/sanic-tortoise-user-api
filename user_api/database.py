from sanic import Sanic
from tortoise.contrib.sanic import register_tortoise


class DatabaseProvider:
    def __init__(
        self, root_folder: str, *, apps: list[str], sanic: Sanic, aerich: bool = False
    ) -> None:
        self._root_folder = root_folder
        self._apps = apps
        self._sanic = sanic
        self._aerich = aerich

    def register(self, db_uri: str, generate_schemas: bool):
        register_tortoise(
            self._sanic,
            db_url=db_uri,
            modules={"models": self._get_models()},
            generate_schemas=generate_schemas,
        )
        return self._generate_config(db_uri)

    def _get_models(self):
        model_list = [
            "{}.{}.models".format(self._root_folder, item) for item in self._apps
        ]
        if self._aerich:
            model_list.append("aerich.models")
        return model_list

    def _generate_config(self, db_uri: str):
        return {
            "connections": {"default": db_uri},
            "apps": {
                "models": {
                    "models": self._get_models(),
                    "default_connection": "default",
                }
            },
        }

__all__ = ["DatabaseProvider"]