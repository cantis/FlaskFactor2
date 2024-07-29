"""Main module of the web application."""

from flask import Flask

from .routes.home import home


def create_app() -> Flask:
    """Create a Flask application."""
    app = Flask(__name__)
    app.secret_key = "head_factor_key"

    # Register blueprints
    app.register_blueprint(home)

    # Create DB and tables
    # create_db()

    return app

app = create_app()