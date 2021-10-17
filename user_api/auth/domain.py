from datetime import datetime, timedelta

from user_api.auth.models import RefreshModel
from user_api.settings import config
from user_api.users.domain import get_user_by_email, get_user_by_id
from user_api.users.schemas import UserSchema
from user_api.utils import functions, password
from user_api.utils.exceptions import (InvalidCredentials,
                                       InvalidOrExpiredToken, ResourceNotFound)
from user_api.utils.functions import fail_with, fail_with_resource_not_found

from . import schemas

EXPIRATION_DEFAULT = 300


@fail_with(ResourceNotFound, InvalidCredentials)
async def authenticate(body: schemas.AuthenticateValidator):
    user = await get_user_by_email(body.username)
    if not password.validate(body.password, user.password):
        raise InvalidCredentials
    payload = generate_token(user.id)
    schema = schemas.TokenSchema.parse_obj(payload)
    return schema, user


async def create_refresh(user_id: int, refresh_token: str):
    await RefreshModel.create(token=refresh_token, user_id=user_id)


async def logout(user_id: int):
    await RefreshModel.filter(user_id=user_id).delete()


@fail_with(ResourceNotFound, InvalidOrExpiredToken)
@fail_with_resource_not_found
async def get_user_from_refresh(body: schemas.RefreshSchema):
    refresh_model = await RefreshModel.get(token=body.refresh_token)
    user = await get_user_by_id(refresh_model.user_id)
    return user


async def refresh(user: UserSchema):
    payload = generate_token(user.id)
    schema = schemas.TokenSchema.parse_obj(payload)
    await RefreshModel.create(token=schema.refresh_token, user_id=user.id)
    return schema, user


@fail_with(ResourceNotFound, InvalidOrExpiredToken)
@fail_with_resource_not_found
async def validate(token: str):
    payload = functions.jwt_decode(token, config.project_key)
    user = await get_user_by_id(payload["user_id"])
    qs = RefreshModel.filter(user_id=user.id)
    refresh = await qs.order_by("-id").first()
    if not refresh:
        raise InvalidOrExpiredToken
    if not functions.validate_jti(payload["jti"], refresh.token, config.project_key):
        raise InvalidOrExpiredToken
    return user


def generate_token(user_id: int, expiration: int = EXPIRATION_DEFAULT):
    now = datetime.utcnow()
    jti = functions.generate_jti(user_id, now, config.project_key)
    access_token = functions.jwt_encode(
        {
            "user_id": user_id,
            "exp": now + timedelta(seconds=expiration),
            "jti": jti,
        },
        config.project_key,
    )
    refresh_token = functions.generate_refresh(jti, config.project_key)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_at": expiration,
    }
