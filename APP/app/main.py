from flask import Flask
from app.config.settings import settings
from app.controllers.main_controller import main_bp
from app.controllers.health_controller import health_bp
from app.controllers.redis_controller import redis_bp
from app.services.redis_service import redis_service
from app.services.mongo_service import mongo_service

def create_app() -> Flask:
    """Application factory – creates and configures the Flask app."""
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(redis_bp)

    # Eagerly connect to backing services
    with app.app_context():
        redis_service.connect()
        mongo_service.connect()

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        debug=settings.APP_DEBUG,
    )
