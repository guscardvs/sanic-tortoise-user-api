from sanic import Blueprint, HTTPResponse, Request
from sanic_ext import openapi, validate

from user_api.auth.decorators import authorize
from user_api.schema import ListSchema

from . import domain, schemas

bp = Blueprint("user", "/user")


@bp.get("/")
@openapi.response(
    200,
    {"application/json": schemas.UserSchema.list()},
)
@authorize
async def list_users(request: Request) -> HTTPResponse:
    return (
        ListSchema[schemas.UserSchema]
        .parse_obj({"data": await domain.list_users()})
        .json_response()
    )


@bp.get("/me")
@openapi.response(200, {"application/json": schemas.UserSchema})
@authorize
async def get_user(request: Request) -> HTTPResponse:
    schema = request.ctx.user
    return schema.json_response()


@bp.post("/")
@openapi.definition(
    body={"application/json": schemas.CreateUserSchema},
    response={"application/json": schemas.UserSchema},
)
@validate(json=schemas.CreateUserValidator)
async def create_user(
    request: Request, body: schemas.CreateUserValidator
) -> HTTPResponse:
    schema = await domain.create_user(body)
    return schema.json_response()


@bp.put("/")
@openapi.definition(
    body={"application/json": schemas.EditUserSchema},
    response={"application/json": schemas.UserSchema},
)
@authorize
@validate(json=schemas.EditUserValidator)
async def edit_user(request: Request, body: schemas.EditUserValidator) -> HTTPResponse:
    schema = await domain.edit_user(request.ctx.user.id, body)
    return schema.json_response()


@bp.patch("/")
@openapi.body({"application/json": schemas.ChangePasswordSchema})
@openapi.response(response=openapi.Response(status=204))
@validate(json=schemas.ChangePasswordSchema)
@authorize
async def change_password(
    request: Request, body: schemas.ChangePasswordSchema
) -> HTTPResponse:
    await domain.change_password(request.ctx.user.id, body)
    return HTTPResponse(status=204)
