from marshmallow import (
    fields, 
    validate, 
    validates, 
    validates_schema, 
    ValidationError, 
    post_load
)

from src.extensions import ma
from src.models.country_code import country_code_db
from src.models.enum import OTPSender

otp_senders = [otp_sender.value for otp_sender in OTPSender]

class GenerateOTPSchema(ma.Schema):
    phone_number = fields.String(
        required=True, 
        validate=validate.Length(min=1, max=100, error="phone_number must between 1 to 100 characters"), 
        error_messages=dict(
            required="phone_number is required"
        )
    )
    country_code = fields.String(
        required=True, 
        validate=validate.Length(min=1, max=100, error="country_code must between 1 to 100 characters"),
        error_messages=dict(
            required="country_code is required"
        )
    )
    otp_sender = fields.String(
        required=True, 
        validate=validate.OneOf(otp_senders, error="Invalid otp_sender"),
        error_messages=dict(
            required="otp_sender is required"
        )
    )

    @validates("country_code")
    def validate_country_code(self, country_code):
        if country_code != "62":
            country_code_check = "+" + country_code
            if not any(
                code.get("code") == country_code_check
                for code in country_code_db
            ):
                raise ValidationError("Invalid country code")

    @validates_schema
    def validate_phone_number_data(self, data, **kwargs):
        len_country_code = len(data["country_code"])
        if data["phone_number"][:len_country_code] != data["country_code"]:
            raise ValidationError("phone_number and country_code not match")
    
generate_otp_schema = GenerateOTPSchema()
