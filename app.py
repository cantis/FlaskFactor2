"""Start point of the application."""

import os

from dotenv import load_dotenv
from flask import Flask

from models import create_db_and_tables

load_dotenv('.env')

def create_app() -> Flask:
    """Flask App factory."""
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')

    # Create DB and tables
    create_db_and_tables()

    # Register blueprints...
    from routes import home
    app.register_blueprint(home.home_bp)

    return app

app = create_app()

if __name__ == '__main__':
    """Run the application."""
    app.run(debug=True, host='127.0.0.1')
