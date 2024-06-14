import os
from logging.config import dictConfig
from dotenv import load_dotenv

load_dotenv()


class Config:
    PROPAGATE_EXCEPTIONS = True
    # Database Config
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASS", "1234")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "otp")
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://"
        + f"{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    OTP_LENGTH = int(os.getenv("OTP_LENGTH"))
    OTP_COOLDOWN_HOURS = int(os.getenv("OTP_COOLDOWN_HOURS"))
    OTP_LIMIT = int(os.getenv("OTP_LIMIT"))
    OTP_EXPIRED = int(os.getenv("OTP_EXPIRED"))

    WA_GATEWAY_URL = os.getenv("WA_GATEWAY_URL")
    WA_PROJECT_ID = os.getenv("WA_PROJECT_ID")
    WA_TYPE = os.getenv("WA_TYPE")


    LOGGING_CONFIG = {
        'version': 1,
        'formatters': {
            'standard': {
                'format': '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'level': 'DEBUG',
            },
            'file': {
                'class': 'logging.FileHandler',
                'filename': 'app.log',
                'formatter': 'standard',
                'level': 'DEBUG',
            },
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': True,
            },
        }
    }

    dictConfig(LOGGING_CONFIG)

CONFIG = Config()
