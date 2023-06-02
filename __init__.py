from flask import Flask
from common.models.database import db
from controllers.auth import auth


def create_app():
    app = Flask(__name__)
    app.config.from_object('settings')

    db.init_app(app)

    app.register_blueprint(auth)

    return app