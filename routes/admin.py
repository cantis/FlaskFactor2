"""Admin routes."""
from flask import Blueprint, render_template

admin_bp = Blueprint('admin', __name__, template_folder='templates')

@admin_bp.route('/')
def index() -> str:
    """Admin home page."""
    return render_template('admin.html')
