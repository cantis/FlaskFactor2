"""Home routes."""

from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__, template_folder='../templates')


@home_bp.route('/')
def index() -> str:
    """Home page."""
    return render_template('home.html')
