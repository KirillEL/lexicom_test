from http import HTTPStatus

from pydantic import BaseModel


class CustomException(Exception):
    code = HTTPStatus.BAD_GATEWAY
    error_code = HTTPStatus.BAD_GATEWAY
    message = HTTPStatus.BAD_GATEWAY.description

    def __init__(self, message=None):
        if message:
            self.message = message


class ExceptionResponseSchema(BaseModel):
    error: str


class NotFoundException(CustomException):
    code = HTTPStatus.NOT_FOUND
    error_code = HTTPStatus.NOT_FOUND
    message = HTTPStatus.NOT_FOUND.description
