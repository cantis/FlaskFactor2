"""Character Routes."""
from flask import Blueprint, render_template

characters_bp = Blueprint('characters', __name__, template_folder='templates')

@characters_bp.route('/')
def index() -> str:
    """Characters home page."""
    return render_template('characters.html')
