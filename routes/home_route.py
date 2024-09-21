"""Home routes."""

from flask import Blueprint, render_template
from sqlalchemy import Null

home_bp = Blueprint('home', __name__, template_folder='templates')


@home_bp.route('/')
def index() -> str:
    """Home page."""
    current_user = None
    current_company = 'Test Company'
    return render_template('home.html', current_user=current_user, current_company=current_company)
