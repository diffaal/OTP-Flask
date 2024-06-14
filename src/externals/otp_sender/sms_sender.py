import requests

from src.config import CONFIG
from src.exceptions.app_exception import InternalErrorException
from src.extensions import logger
from src.externals.otp_sender import OTPSender

class SMSSender(OTPSender):
    async def send_otp(self, phone_number, otp_code):
        pass