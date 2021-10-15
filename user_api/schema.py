import re
from typing import Generic, Optional, TypeVar

import ujson
from pydantic.generics import GenericModel
from sanic import json
from sanic_ext import openapi
from tortoise.contrib.pydantic.base import PydanticModel
from tortoise.models import Model

pattern = re.compile("_([A-Z])")

T = TypeVar("T")


class Schema(PydanticModel):
    class Config(PydanticModel.Config):
        json_loads = ujson.loads
        json_dumps = ujson.dumps

    @classmethod
    def list(cls, key: Optional[str] = None):
        key = key or "data"
        return openapi.Object({key: openapi.Array(cls)})

    def json_response(self, status: int = 200):
        return json(self, dumps=Schema.json)

    @classmethod
    async def from_tortoise_orm(cls: type[T], obj: "Model") -> T:
        return await super().from_tortoise_orm(obj)  # type: ignore


class ListSchema(Generic[T], GenericModel, Schema):
    data: list[T]
