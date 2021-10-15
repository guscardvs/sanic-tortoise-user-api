from user_api.utils import password
from user_api.utils.functions import fail_with_resource_not_found

from .models import UserModel
from .schemas import (ChangePasswordSchema, CreateUserValidator, DescribeUser,
                      EditUserValidator, UserSchema)


async def create_user(create_user: CreateUserValidator):
    instance = await UserModel.create(
        **create_user.dict(exclude={"password"}),
        password=password.hash(create_user.password)
    )
    return UserSchema.from_orm(instance)


async def list_users():
    return [UserSchema.from_orm(item) for item in await UserModel.filter()]


@fail_with_resource_not_found
async def get_user_by_id(id: int):
    instance = await UserModel.get(id=id)
    return UserSchema.from_orm(instance)


@fail_with_resource_not_found
async def edit_user(id: int, edit_user: EditUserValidator):
    instance = await UserModel.get(id=id)
    instance.update_from_dict(edit_user.dict(exclude_unset=True))
    await instance.save()
    return UserSchema.from_orm(instance)


@fail_with_resource_not_found
async def change_password(id: int, change_password: ChangePasswordSchema):
    instance = await UserModel.get(id=id)
    instance.update_from_dict({"password": password.hash(change_password.password)})
    await instance.save()


@fail_with_resource_not_found
async def get_user_by_email(email: str):
    instance = await UserModel.get(email=email)
    return DescribeUser.from_orm(instance)
