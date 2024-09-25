"""Home routes."""

import flask_login
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_wtf import FlaskForm
from werkzeug import Response
from wtforms import PasswordField, StringField
from wtforms.validators import Email, InputRequired

from services.players_service import get_player_by_email, validate_password

home_bp = Blueprint('home', __name__, template_folder='templates')


class LoginPlayerForm(FlaskForm):
    """Login player form."""

    email = StringField('Email', validators=[InputRequired('Email is required'), Email('Invalid email')])
    password = PasswordField('Password', validators=[InputRequired('Password is required')])
    remember = StringField('Remember Me')


@home_bp.route('/')
def index() -> str:
    """Home page."""
    current_user = None
    current_company = 'Test Company'
    return render_template('home/home.html', current_user=current_user, current_company=current_company)


@home_bp.route('/login', methods=['GET'])
def login_get() -> str:
    """Show the player login html page."""
    form = LoginPlayerForm()
    return render_template('home/login.html', form=form)


@home_bp.route('/login', methods=['POST'])
def login_post() -> Response:
    """Process player login."""
    form = LoginPlayerForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = bool(form.remember.data) if form.remember.data else False
        if validate_password(email, password):
            player = get_player_by_email(email)
            flask_login.login_user(player, remember=remember)
            flash(f'Player {player.name} logged in successfully', 'success')
            return redirect(url_for('players.players_list'), code=200)
    flash('Invalid email or password', 'danger')
    return redirect(url_for('home.login_get'), code=401)


@home_bp.route('/logout')
def logout() -> Response:
    """Logout the player."""
    flask_login.logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('home.index'))
