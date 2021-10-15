import typing
from datetime import date

from pydantic import EmailStr
from sanic_ext import openapi

from user_api.schema import Schema


class UserSchema(Schema):
    id: int
    email: str
    birth_date: date
    first_name: str
    last_name: str


class CreateUserValidator(Schema):
    email: EmailStr
    password: str
    birth_date: date
    first_name: str
    last_name: str


CreateUserSchema = openapi.Object(
    {
        "email": openapi.Email(),
        "password": openapi.Password(),
        "birth_date": openapi.Date(),
        "first_name": openapi.String(),
        "last_name": openapi.String(),
    }
)


class EditUserValidator(Schema):
    email: typing.Optional[EmailStr] = None
    birth_date: typing.Optional[date] = None
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None


EditUserSchema = openapi.Object(
    {
        "email": openapi.Email(),
        "birth_date": openapi.Date(),
        "first_name": openapi.String(),
        "last_name": openapi.String(),
    }
)


class ChangePasswordSchema(Schema):
    password: str


class DescribeUser(UserSchema):
    password: str
