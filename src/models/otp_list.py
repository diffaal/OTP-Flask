import sqlalchemy as sa

from src.exceptions.app_exception import DatabaseException
from src.models.base_model import BaseModel

class OtpList(BaseModel):
    __tablename__ = "otp_list"

    phone_number = sa.Column(sa.String(200), nullable=False)
    otp_code = sa.Column(sa.String(50), nullable=False)
    expired_time = sa.Column(sa.DateTime(), nullable=False)
    is_used = sa.Column(sa.Boolean(), nullable=False)

    @classmethod
    def get_otp_list_by_phone_number(cls, phone_number) -> 'OtpList':
        try:
            return cls.query.filter(
                cls.phone_number == phone_number
            ).first()
        except Exception as e:
            DatabaseException(e)
