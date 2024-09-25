"""Player Routes."""

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from werkzeug import Response
from wtforms import PasswordField, StringField
from wtforms.validators import Email, InputRequired

from services.players_service import (
    add_player,
    delete_player,
    get_all_players,
    get_player_by_id,
    update_player,
)

players_bp = Blueprint('players', __name__, template_folder='templates')


class AddPlayerForm(FlaskForm):
    """Add player form."""

    name = StringField('Name', validators=[InputRequired('Name is required')])
    email = StringField('Email', validators=[InputRequired('Email is required'), Email('Invalid email')])
    password = PasswordField('Password')


class UpdatePlayerForm(FlaskForm):
    """Update player form."""

    name = StringField('Name')
    email = StringField('Email', validators=[Email('Invalid email')])
    current_password = PasswordField('Current Password')
    new_password = PasswordField('Password')


@players_bp.route('/')
def players_list() -> str:
    """List all players."""
    players = get_all_players()
    return render_template('players/player_list.html', players=players)


@players_bp.route('/player_add', methods=['GET'])
def player_add_get() -> str:
    """Show the player add html page."""
    return render_template('players/player_add.html', form=AddPlayerForm())


@players_bp.route('/players', methods=['POST'])
def player_add_post() -> Response:
    """Process the player add form and back to the player list."""
    form = AddPlayerForm()
    if form.validate_on_submit():
        player_data = {
            'name': form.name.data,
            'email': form.email.data,
            'password': form.password.data,
        }
        new_player = add_player(player_data)
        flash(f'Player {new_player.name} added successfully', 'success')
    return redirect(url_for('players.player_list'))


@players_bp.route('/players/<int:player_id>', methods=['GET'])
def player_update_get(player_id) -> str:
    """Get a player for update."""
    player = get_player_by_id(player_id)
    if not player:
        return abort(404, f'Player with id {player_id} not found')
    return render_template('players/player_update.html', form=UpdatePlayerForm(data=player))


@players_bp.route('/players/<int:player_id>', methods=['PUT'])
def player_update_put(player_id) -> Response:
    """Modify a player."""
    form = UpdatePlayerForm()
    if form.validate_on_submit():
        update_data = {
            'name': form.name.data,
            'email': form.email.data,
            'password': form.password.data,
        }
        updated_player = update_player(player_id, update_data)
        if updated_player:
            flash(f'Player {updated_player.name} updated successfully', 'success')
        else:
            abort(404)
    return redirect(url_for('players.player_list'))


@players_bp.route('/players/<int:player_id>', methods=['DELETE'])
def player_delete(player_id) -> Response:
    """Remove a player."""
    player = delete_player(player_id)
    if not player:
        abort(404, f'Player with id {player_id} not found')
    flash(f'Player {player.name} deleted successfully', 'success')
    return redirect(url_for('players.player_list'))
