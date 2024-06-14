from flask import Flask
from marshmallow import ValidationError

from src.exceptions.app_exception import OTPFlaskException
from src.exceptions.error_handler import (
    app_error_handler, 
    exception_handler,
    validation_error_handler
)

def register_error_handler(app: Flask):
    app.register_error_handler(OTPFlaskException, app_error_handler)
    app.register_error_handler(Exception, exception_handler)
    app.register_error_handler(ValidationError, validation_error_handler)
