from flask import Flask
from src.blueprints.otp import otp_bp

def register_blueprints(app: Flask):
    app.register_blueprint(otp_bp)
