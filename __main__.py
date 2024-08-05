"""Start point of the application."""

import os

from dotenv import load_dotenv
from flask import Flask

from models import create_db_and_tables
from web.routes import home

load_dotenv('.env')


def create_app() -> Flask:
    """Create a Flask application."""
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')

    # Create DB and tables
    create_db_and_tables()

    # Register blueprints...
    app.register_blueprint(home)

    return app


app = create_app()

if __name__ == '__main__':
    """Run the application."""
    print('\n App Running and website is available at http://localhost:5000/')
    app.run(debug=True, host='127.0.0.1')
