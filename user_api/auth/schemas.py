from pydantic import EmailStr
from sanic_ext import openapi

from user_api.schema import Schema


class TokenSchema(Schema):
    access_token: str
    refresh_token: str
    expires_at: int


class AuthenticateValidator(Schema):
    username: EmailStr
    password: str


AuthenticateSchema = openapi.Object(
    {"username": openapi.Email(), "password": openapi.Password()}
)


class RefreshSchema(Schema):
    refresh_token: str
