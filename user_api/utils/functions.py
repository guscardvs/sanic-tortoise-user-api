import hashlib
import hmac
import os
import typing
from datetime import datetime
from functools import wraps
from inspect import iscoroutinefunction

from jose import jwt
from tortoise.exceptions import DoesNotExist
from typing_extensions import ParamSpec, TypedDict, TypeGuard

from .exceptions import InvalidOrExpiredToken, ResourceNotFound

ExcType = type[Exception]
T = typing.TypeVar("T")
P = ParamSpec("P")


def _async_wrap(
    source: ExcType,
    target: ExcType,
    func: typing.Callable[P, typing.Awaitable[T]],
) -> typing.Callable[P, typing.Awaitable[T]]:
    @wraps(func)
    async def inner(*args: P.args, **kwargs: P.kwargs) -> T:
        try:
            return await func(*args, **kwargs)
        except source as err:
            print(err)
            raise target from err

    return inner


def sync_wrap(
    source: ExcType,
    target: ExcType,
    func: typing.Callable[P, T],
) -> typing.Callable[P, T]:
    @wraps(func)
    def inner(*args: P.args, **kwargs: P.kwargs) -> T:
        try:
            return func(*args, **kwargs)
        except source as err:
            raise target from err

    return inner


def is_coroutine(
    func: typing.Callable[P, typing.Union[T, typing.Awaitable[T]]]
) -> TypeGuard[typing.Callable[P, typing.Awaitable[T]]]:
    return iscoroutinefunction(func)


def fail_with(source: ExcType, target: ExcType):
    def outer(func: typing.Callable[P, T]) -> typing.Callable[P, T]:
        if is_coroutine(func):
            return _async_wrap(source, target, func)
        return sync_wrap(source, target, func)

    return outer


fail_with_resource_not_found = fail_with(DoesNotExist, ResourceNotFound)


def project_key_generator():
    return hmac.new(os.urandom(32), os.urandom(32), hashlib.sha512).hexdigest()


class _JWTEncodePayload(TypedDict):
    user_id: int
    exp: datetime
    jti: str


def jwt_encode(payload: _JWTEncodePayload, key: str):
    return jwt.encode(payload, key)


def jwt_decode(token: str, key: str) -> _JWTEncodePayload:
    try:
        return jwt.decode(token, key)  # type: ignore
    except jwt.JWTError as err:
        raise InvalidOrExpiredToken from err


def generate_jti(user_id: int, dt: datetime, key: str) -> str:
    return hmac.new(
        key.encode(),
        ":".join((str(user_id), str(int(datetime.timestamp(dt))))).encode(),
        hashlib.sha512,
    ).hexdigest()


def validate_jti(jti: str, refresh: str, key: str):
    return generate_refresh(jti, key) == refresh


def generate_refresh(jti: str, key: str):
    return hmac.new(jti.encode(), key.encode(), hashlib.sha512).hexdigest()
