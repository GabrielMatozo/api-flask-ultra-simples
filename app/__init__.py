import time
from sqlalchemy import text
from flasgger import Swagger
from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.config import Config
from app.models import db
from app.errors import register_error_handlers
from app.routes.carros import carros_bp

limiter = Limiter(key_func=get_remote_address, default_limits=["100/hour"])


def create_app(config_override=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if config_override:
        app.config.update(config_override)

    CORS(app)
    Swagger(app)
    limiter.init_app(app)
    db.init_app(app)
    app.register_blueprint(carros_bp)
    register_error_handlers(app)

    @app.route("/health")
    def health():
        return jsonify(status="ok")

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
