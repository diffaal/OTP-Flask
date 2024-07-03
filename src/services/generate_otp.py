from datetime import datetime, timedelta

from src.config import CONFIG
from src.externals.otp_sender.wa_sender import WASender
from src.externals.otp_sender.sms_sender import SMSSender
from src.helpers.otp_activity_validator import OTPActivityValidator
from src.helpers.otp_code_generator import OTPCodeGenerator
from src.models.enums import ActivityType, OTPSender
from src.models.otp_list import OtpList
from src.tools.response import make_otp_response_data

class GenerateOTPService:
    def generate_otp(self, request_data):
        phone_number = request_data.get("phone_number")
        otp_sender = request_data.get("otp_sender")

        gen_otp_activity =  OTPActivityValidator.validate_otp_activity(phone_number, ActivityType.GENERATE_OTP.value)
        _ = OTPActivityValidator.validate_otp_activity(phone_number, ActivityType.VALIDATE_OTP.value)
        
        otp_code = OTPCodeGenerator.generate_otp_code()

        if otp_sender == OTPSender.WHATSAPP.value:
            otp_sender_service = WASender()
        elif otp_sender == OTPSender.SMS.value:
            otp_sender_service = SMSSender()
        
        otp_sender_service.send_otp(phone_number, otp_code)

        self.insert_otp_code(phone_number, otp_code)

        if not gen_otp_activity.attempt:
            gen_otp_activity.attempt = 1
        else:
            gen_otp_activity.attempt += 1
        
        gen_otp_activity.update()

        return make_otp_response_data(gen_otp_activity.attempt)

    def insert_otp_code(self, phone_number, otp_code):
        now = datetime.now()
        expired_minute = timedelta(minutes=CONFIG.OTP_EXPIRED)
        otp_expired = now + expired_minute

        otp_list = OtpList.get_otp_list_by_phone_number(phone_number)
        if otp_list:
            otp_list.otp_code = otp_code
            otp_list.is_used = False
            otp_list.expired_time = otp_expired

            otp_list.update()
        else:
            new_otp_list = OtpList(
                phone_number=phone_number,
                otp_code=otp_code,
                is_used=False,
                expired_time=otp_expired
            )
            new_otp_list.add()

generate_otp_service = GenerateOTPService()
