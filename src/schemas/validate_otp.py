from marshmallow import fields, validate

from src.config import Config
from src.extensions import ma

CONFIG = Config()


class ValidateOTPSchema(ma.Schema):
    phone_number = fields.String(
        required=True, 
        validate=validate.Length(min=1, max=100, error="phone_number must between 1 to 100 characters"), 
        error_messages=dict(
            required="phone_number is required"
        )
    )
    otp_code = fields.String(
        required=True, 
        validate=validate.Length(equal=CONFIG.OTP_LENGTH, error=f"otp_code must be {CONFIG.OTP_LENGTH} characters"),
        error_messages=dict(
            required="otp_code is required"
        )
    )

validate_otp_schema = ValidateOTPSchema()
