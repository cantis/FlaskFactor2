"""Player Routes."""
from flask import Blueprint, render_template

players_bp = Blueprint('players', __name__, template_folder='templates')

@players_bp.route('/')
def index() -> str:
    """Players home page."""
    return render_template('players.html')