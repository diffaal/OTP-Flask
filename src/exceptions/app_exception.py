from http import HTTPStatus
from traceback import format_exc

from src.extensions import db, logger
from src.models.enums import ResponseMessage
from src.tools.response import make_json_response

class OTPFlaskException(Exception):
    def __init__(self, code, message, data) -> None:
        self.code = code
        self.message = message
        self.data = data
    
    def process_error_response(self):
        error_logger(self)
        db.session.rollback()
        return make_json_response(self.code, self.message, self.data)
        

class BadRequestException(OTPFlaskException):
    def __init__(self, message, data) -> None:
        super().__init__(HTTPStatus.BAD_REQUEST, message, data)

class NotFoundException(OTPFlaskException):
    def __init__(self, message, data) -> None:
        super().__init__(HTTPStatus.NOT_FOUND, message, data)

class UnauthorizedException(OTPFlaskException):
    def __init__(self, message, data) -> None:
        super().__init__(HTTPStatus.UNAUTHORIZED, message, data)

class InvalidRequestException(OTPFlaskException):
    def __init__(self, message, data) -> None:
        super().__init__(HTTPStatus.UNPROCESSABLE_ENTITY, message, data)

class InternalErrorException(OTPFlaskException):
    def __init__(self, message, data, error_cause: Exception) -> None:
        super().__init__(HTTPStatus.INTERNAL_SERVER_ERROR, message, data)
        self.error_cause = error_cause
    
    def process_error_response(self):
        if self.error_cause:
            error_logger(self.error_cause, True)
        else:
            error_logger(self)
        db.session.rollback()
        return make_json_response(self.code, self.message, self.data)

class DatabaseException(InternalErrorException):
    def __init__(self, error_cause: Exception, data = None) -> None:
        super().__init__(ResponseMessage.DATABASE_ERROR.value, data, error_cause)

def error_logger(e, traceback = False):
    logger.error(f"Exception Type::{type(e).__name__}")
    logger.error(f"Syserr::{e}")
    if traceback:
        logger.error(f"Traceback::{format_exc()}")
