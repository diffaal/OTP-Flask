import secrets
import string

from src.config import CONFIG

class OTPCodeGenerator:
    def generate_otp_code():
        otp_code = ""
        digits = string.digits
        for _ in range(CONFIG.OTP_LENGTH):
            otp_code += str(secrets.choice(digits))
        
        return otp_code
