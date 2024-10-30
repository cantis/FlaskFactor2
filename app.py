"""Start point of the application, flask app factory."""

import logging
import os
import traceback

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_login import LoginManager

from models import Player, create_db_and_tables
from routes import admin_route, characters_route, home_route, players_route, transactions_route
from services import players_service

load_dotenv('.env')


def create_app() -> Flask:
    """Flask App factory."""
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('flask_factor.log'),
            logging.StreamHandler(),
        ],
    )
    logger = logging.getLogger(__name__)
    logger.info('Application startup')

    # Create DB and tables
    create_db_and_tables()

    # Register blueprints...
    app.register_blueprint(home_route.home_bp, url_prefix='/')
    app.register_blueprint(admin_route.admin_bp, url_prefix='/admin')
    app.register_blueprint(characters_route.characters_bp, url_prefix='/characters')
    app.register_blueprint(transactions_route.transactions_bp, url_prefix='/transactions')
    app.register_blueprint(players_route.players_bp, url_prefix='/players')

    return app


# Create the app
app = create_app()

# Setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view = 'players.login'


@app.errorhandler(Exception)
def handle_exception(error: Exception) -> str:
    """Handle all exceptions."""
    trace = traceback.format_exc() if app.debug else None
    return render_template('error.html', error=error, trace=trace)


@login_manager.user_loader
def load_user(email: str) -> Player:
    """Load the user."""
    return players_service.get_player_by_email(email)


if __name__ == '__main__':
    """Run the application."""
    app.run(debug=True, host='127.0.0.1')
