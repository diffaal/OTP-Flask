import psycopg2.errorcodes
import sqlalchemy as sa
import sqlalchemy.exc

from src.exceptions.app_exception import DatabaseException, InternalErrorException
from src.models.base_model import BaseModel
from src.models.enum import ActivityType, ResponseMessage

class OtpActivity(BaseModel):
    __tablename__ = "otp_activity"

    phone_number = sa.Column(sa.String(200), nullable=False)
    activity_type: ActivityType = sa.Column(sa.String(200), nullable=False)
    attempt = sa.Column(sa.Integer(), nullable=True)

    @classmethod
    def lock_otp_activity(cls, phone_number, activity_type) -> 'OtpActivity':
        try:
            return cls.query.with_for_update(
                nowait=True
            ).filter(
                cls.phone_number == phone_number, 
                cls.activity_type == activity_type
            ).order_by(cls.updated_at.desc()).first()
        except sqlalchemy.exc.OperationalError as e:
            if e.orig.pgcode == psycopg2.errorcodes.LOCK_NOT_AVAILABLE:
                raise InternalErrorException(ResponseMessage.OTP_BEING_PROCESSED.value, None, e)
            raise DatabaseException(e)
        except Exception as e:
            raise DatabaseException(e)

    