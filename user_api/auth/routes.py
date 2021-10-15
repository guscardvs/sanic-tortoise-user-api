from sanic import Blueprint, HTTPResponse, Request
from sanic_ext import openapi, validate

from user_api.auth.decorators import authorize

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
    result = await domain.authenticate(body)
    return result.json_response()


@bp.post("/refresh")
@openapi.definition(
    body={"application/json": schemas.RefreshSchema},
    response={"application/json": schemas.TokenSchema},
)
@validate(json=schemas.RefreshSchema)
async def refresh(request: Request, body: schemas.RefreshSchema) -> HTTPResponse:
    result = await domain.refresh(body)
    return result.json_response()


@bp.delete("/logout")
@openapi.response(
    response=openapi.Response(status=204),
)
@authorize
async def logout(request: Request):
    await domain.logout(request.ctx.user.id)
    return HTTPResponse(status=204)
