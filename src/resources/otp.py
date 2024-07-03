from flask import (
    Response,
    request
)
from flask_restful import Resource
from http import HTTPStatus

from src.models.enums import ResponseMessage
from src.schemas.generate_otp import generate_otp_schema
from src.schemas.validate_otp import validate_otp_schema
from src.services.generate_otp import generate_otp_service
from src.services.validate_otp import validate_otp_service
from src.tools.response import make_json_response


class GenerateOTP(Resource):
    def post(self) -> Response:
        request_data = generate_otp_schema.load(request.json)
        result_data = generate_otp_service.generate_otp(request_data)
        return make_json_response(HTTPStatus.OK, ResponseMessage.SUCCESS.value, result_data)

class ValidateOTP(Resource):
    def post(self) -> Response:
        request_data = validate_otp_schema.load(request.json)
        result_data = validate_otp_service.validate_otp(request_data)
        return make_json_response(HTTPStatus.OK, ResponseMessage.SUCCESS.value, result_data)
