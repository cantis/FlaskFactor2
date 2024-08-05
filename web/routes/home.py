"""Home routes."""

from flask import Blueprint, render_template

home = Blueprint('home', __name__)


@home.route('/')
def index() -> str:
    """Home page."""
    return render_template('home.html')
