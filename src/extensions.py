from flask import Flask, request, Response
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from logging import Logger

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
logger = Logger("OTP FLASK")

def register_extensions(app: Flask):
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    logger.addHandler(app.logger)

def before_request():
    logger.info(f'Starting request {request.method} {request.path}')

def after_request(response: Response):
    logger.info(f'Finished request {request.method} {request.path} with status {response.status_code}')
    return response

def teardown_request(exception):
    db.session.remove()

def register_after_before_request(app: Flask):
    app.before_request(before_request)
    app.teardown_request(teardown_request)
