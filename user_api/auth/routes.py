from datetime import datetime

from sanic import Blueprint, HTTPResponse, Request
from sanic_ext import openapi, validate

from user_api.auth.decorators import authorize
from user_api.utils.functions import mask_email

from . import domain, schemas

bp = Blueprint("auth", "/auth")


@bp.post("/token")
@openapi.definition(
    body={"application/json": schemas.AuthenticateSchema},
    response={"application/json": schemas.TokenSchema},
)
@validate(json=schemas.AuthenticateValidator)
async def authenticate(
    request: Request, body: schemas.AuthenticateValidator
) -> HTTPResponse:
    schema, user = await domain.authenticate(body)
    await domain.logout(user.id)
    await domain.create_refresh(user.id, schema.refresh_token)
    request.app.ctx.logger.info(
        "[%s] - %s: %s",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Token claim made by: ",
        mask_email(user.email),
    )
    return schema.json_response()


@bp.post("/refresh")
@openapi.definition(
    body={"application/json": schemas.RefreshSchema},
    response={"application/json": schemas.TokenSchema},
)
@validate(json=schemas.RefreshSchema)
async def refresh(request: Request, body: schemas.RefreshSchema) -> HTTPResponse:
    user = await domain.get_user_from_refresh(body)
    await domain.logout(user.id)
    schema, user = await domain.refresh(user)
    request.app.ctx.logger.info(
        "[%s] - %s: %s",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Refresh Token claim made by: ",
        mask_email(user.email),
    )
    return schema.json_response()


@bp.delete("/logout")
@openapi.response(
    response=openapi.Response(status=204),
)
@authorize
async def logout(request: Request):
    await domain.logout(request.ctx.user.id)
    return HTTPResponse(status=204)
