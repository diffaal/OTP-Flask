from datetime import datetime

from src.exceptions.app_exception import BadRequestException
from src.helpers.otp_activity_validator import OTPActivityValidator
from src.models.enum import ActivityType, ResponseMessage
from src.models.otp_list import OtpList
from src.tools.response import make_otp_response_data

class ValidateOTPService:
    def validate_otp(self, request_data):
        phone_number = request_data.get("phone_number")
        otp_code = request_data.get("otp_code")

        val_otp_activity = OTPActivityValidator.validate_otp_activity(phone_number, ActivityType.VALIDATE_OTP.value)

        err_message = self.validate_otp_code(phone_number, otp_code)
        if err_message:
            if not val_otp_activity.attempt:
                val_otp_activity.attempt = 1
            else:
                val_otp_activity.attempt += 1
            
            val_otp_activity.update()
            
            result_data = make_otp_response_data(val_otp_activity.attempt)
            raise BadRequestException(err_message, result_data)
        
        return make_otp_response_data(val_otp_activity.attempt)
    
    def validate_otp_code(self, phone_number, otp_code):
        otp_list = OtpList.get_otp_list_by_phone_number(phone_number)

        if not otp_list:
            raise BadRequestException(ResponseMessage.OTP_CODE_NOT_FOUND.value, None)

        now = datetime.now()
        if now > otp_list.expired_time:
            return ResponseMessage.OTP_EXPIRED.value
        
        if otp_list.is_used:
            return ResponseMessage.OTP_USED.value
        
        if otp_list.otp_code != otp_code:
            return ResponseMessage.INVALID_OTP.value
        
        otp_list.is_used = True
        otp_list.update()

        return None

validate_otp_service = ValidateOTPService()
