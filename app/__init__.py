import time
from sqlalchemy import text
from flask import Flask
from app.config import Config
from app.models import db
from app.errors import register_error_handlers
from app.routes.carros import carros_bp


def create_app(config_override=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if config_override:
        app.config.update(config_override)

    db.init_app(app)
    app.register_blueprint(carros_bp)
    register_error_handlers(app)

    with app.app_context():
        _wait_for_db()
        db.create_all()

    return app


def _wait_for_db():
    for attempt in range(15):
        try:
            db.session.execute(text("SELECT 1"))
            db.session.commit()
            return
        except Exception:
            if attempt < 14:
                time.sleep(1)
