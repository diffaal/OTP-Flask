from flask import Response
from http import HTTPStatus
from marshmallow import ValidationError

from src.exceptions.app_exception import OTPFlaskException, error_logger
from src.extensions import db
from src.tools.response import make_json_response

from src.models.enum import ResponseMessage

def app_error_handler(e: OTPFlaskException) -> Response:
    return e.process_error_response()

def validation_error_handler(e: ValidationError) -> Response:
    return make_json_response(HTTPStatus.UNPROCESSABLE_ENTITY, e.messages, None)

def exception_handler(e: Exception) -> Response:
    error_logger(e, True)
    db.session.rollback()
    return make_json_response(HTTPStatus.INTERNAL_SERVER_ERROR, ResponseMessage.INTERNAL_SERVER_ERROR.value, None)