"""Transactions routes."""
from flask import Blueprint, render_template

transactions_bp = Blueprint('transactions', __name__, template_folder='templates')

@transactions_bp.route('/')
def index() -> str:
    """Transactions home page."""
    return render_template('transactions.html')
