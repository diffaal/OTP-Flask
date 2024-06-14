from flask import Flask

from src.blueprints import register_blueprints
from src.exceptions import register_error_handler
from src.extensions import register_extensions, register_after_before_request
from src.config import Config

def create_app() -> Flask:
    app = Flask("OTP FLASK")
    app.config.from_object(Config)

    with app.app_context():
        
        register_extensions(app)
        register_blueprints(app)
        register_error_handler(app)
        register_after_before_request(app)

        return app
