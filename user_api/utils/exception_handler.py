from typing import TypedDict, Union

from sanic import Blueprint, Request, json
from sanic.blueprint_group import BlueprintGroup
from sanic_ext.exceptions import ValidationError

from . import exceptions


class ExceptionHandler:
    def __init__(self, bp: Union[Blueprint, BlueprintGroup]) -> None:
        self.bp = bp

    def setup(self):
        self.bp.exception(exceptions.ResourceNotFound)(self.resource_not_found)
        self.bp.exception(exceptions.InvalidOrExpiredToken)(
            self.invalid_or_expired_token
        )
        self.bp.exception(exceptions.InvalidCredentials)(self.invalid_credentials)
        self.bp.exception(ValidationError)(self.validation_error)

    class _ResponseBody(TypedDict):
        status: int
        description: str
        path: str

    def generate_response(
        self,
        status: int = 400,
        /,
        *,
        path: str,
        description: str = "",
    ) -> _ResponseBody:
        return {"status": status, "path": path, "description": description}

    def resource_not_found(self, request: Request, exception):
        status = 404
        return json(
            self.generate_response(
                status, path=request.path, description="resource not found in server"
            ),
            status,
            headers={"Resource-Not-Found": request.path},
        )

    def validation_error(self, request: Request, exception: ValidationError):
        status = 422
        return json(
            self.generate_response(
                status, path=request.path, description=exception.args[0]
            ),
            status,
            headers={"Invalid-Request": request.path},
        )

    def invalid_or_expired_token(self, request: Request, exception):
        status = 403
        return json(
            self.generate_response(
                status, path=request.path, description="invalid or expired token"
            ),
            status,
            headers={"Authorization-Error": request.path},
        )

    def invalid_credentials(self, request: Request, exception):
        status = 401
        return json(
            self.generate_response(
                status, path=request.path, description="invalid credentials"
            ),
            status,
            headers={"Authorization-Error": request.path},
        )
