import json
import requests

from src.config import CONFIG
from src.exceptions.app_exception import InternalErrorException
from src.extensions import logger
from src.externals.otp_sender import OTPSender
from src.models.enum import ResponseMessage

class WASender(OTPSender):
    def __init__(self) -> None:
        self.wa_gateway_url = CONFIG.WA_GATEWAY_URL
        self.wa_project_id = CONFIG.WA_PROJECT_ID
        self.wa_type = CONFIG.WA_TYPE
    
    def send_otp(self, phone_number, otp_code):
        req_body = {
            "channelId": "EFORM", 
            "partnerId": self.wa_project_id, 
            "projectType": self.wa_type, 
            "mobileNum": phone_number, 
            "param1": otp_code, 
            "param2": "", 
            "param3": "",
            "jenis_rekening": ""
        }

        logger.info(f"Whatsapp Gateway Send Message URL: {self.wa_gateway_url}")
        logger.info(f"Whatsapp Gateway Send Message Request Body:\n{json.dumps(req_body, indent=2)}")

        try:
            response = requests.post(
                self.wa_gateway_url,
                json=req_body,
            )
        except requests.ConnectionError as e:
            logger.error(ResponseMessage.WA_SENDER_CONNECTION_ERROR.value)
            raise InternalErrorException(ResponseMessage.WA_SENDER_CONNECTION_ERROR.value, None, e)
        except requests.Timeout as e:
            logger.error(ResponseMessage.WA_SENDER_TIMEOUT.value)
            raise InternalErrorException(ResponseMessage.WA_SENDER_TIMEOUT.value, None, e)

        status_code = response.status_code
        logger.info(f"Whatsapp Gateway Send Message Response Status Code: {status_code}")
        if status_code == 500:
            logger.error(ResponseMessage.WA_SENDER_INTERNAL_ERROR.value)
            raise InternalErrorException(ResponseMessage.WA_SENDER_INTERNAL_ERROR.value, None, None)
        
        res_body = response.json()
        logger.info(f"Whatsapp Gateway Send Message Response Body:\n{json.dumps(res_body, indent=2)}")

        error_code = res_body.get("errorCode", "")
        error_message = res_body.get("errorMessage", "")
        if error_code != "200":
            logger.error(f"WA Sender:: {error_message}")
            raise InternalErrorException(f"WA Sender:: {error_message}", None, None)
