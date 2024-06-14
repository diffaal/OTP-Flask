from flask import Blueprint
from flask_restful import Api

from src.resources.otp import GenerateOTP, ValidateOTP

otp_bp = Blueprint("otp_bp", __name__, url_prefix="/api/v1/otp")
otp_api = Api(otp_bp)
otp_api.add_resource(GenerateOTP, "/generate")
otp_api.add_resource(ValidateOTP, "/validate")
