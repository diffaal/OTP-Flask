from datetime import datetime, timedelta

from src.config import CONFIG
from src.exceptions.app_exception import BadRequestException
from src.models.enum import ActivityType, ResponseMessage
from src.models.otp_activity import OtpActivity
from src.tools.response import make_otp_response_data


class OTPActivityValidator:
    @staticmethod
    def validate_otp_activity(phone_number, activity_type):
        otp_activity = OtpActivity.lock_otp_activity(phone_number, activity_type)
        if otp_activity:
            now = datetime.now()
            cooldown_time = timedelta(hours=CONFIG.OTP_COOLDOWN_HOURS)
            diff_hours = now - otp_activity.updated_at

            if diff_hours <= cooldown_time:
                if otp_activity.attempt >= CONFIG.OTP_LIMIT:
                    resp_data = make_otp_response_data(otp_activity.attempt)

                    if activity_type == ActivityType.GENERATE_OTP.value:
                        err_message = ResponseMessage.TOO_MANY_GENERATE_OTP.value
                    else:
                        err_message = ResponseMessage.TOO_MANY_FAILED_VALIDATE_OTP.value
                        
                    raise BadRequestException(err_message, resp_data)
            else:
                otp_activity.attempt = 0
        else:
            new_otp_activity = OtpActivity(
                phone_number=phone_number,
                activity_type=activity_type,
                attempt=0
            )
            new_otp_activity.add()

            otp_activity = OtpActivity.lock_otp_activity(phone_number, activity_type)
        
        return otp_activity
        