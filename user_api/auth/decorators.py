import typing
from functools import wraps

from sanic import Request
from sanic_ext import openapi
from typing_extensions import Concatenate, ParamSpec

from user_api.utils.exceptions import InvalidOrExpiredToken
from user_api.utils.functions import is_coroutine

from . import domain

T = typing.TypeVar("T")
P = ParamSpec("P")


def authorize(
    func: typing.Callable[Concatenate[Request, P], T]
) -> typing.Callable[Concatenate[Request, P], T]:
    @openapi.parameter("Authorization", str, "header", required=True)
    @wraps(func)
    async def inner(request: Request, *args: P.args, **kwargs: P.kwargs):
        token = request.token  # type: typing.Optional[str]
        if not token:
            raise InvalidOrExpiredToken
        user = await domain.validate(token.removeprefix("Bearer "))
        request.ctx.user = user
        if is_coroutine(func):
            return await func(request, *args, **kwargs)  # type: ignore
        return func(request, *args, **kwargs)

    return inner
