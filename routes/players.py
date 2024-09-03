"""Player Routes."""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from werkzeug import Response
from wtforms import PasswordField, StringField
from wtforms.validators import Email, InputRequired

from services.players_service import add_player, delete_player, get_all_players, get_player, update_player

players_bp = Blueprint('players', __name__, template_folder='templates')


class AddPlayerForm(FlaskForm):
    """Add player form."""

    name = StringField('Name', validators=[InputRequired('Name is required')])
    email = StringField('Email', validators=[InputRequired('Email is required'), Email('Invalid email')])
    password = PasswordField('Password')


@players_bp.route('/')
def player_list() -> str:
    """List all players."""
    players = get_all_players()
    return render_template('players/player_list.html', players=players)
    return render_template('players/player_list.html')


@players_bp.route('/player_add', methods=['GET'])
def player_add_form() -> str:
    """Show the player add template."""
    return render_template('players/player_add.html', form=AddPlayerForm())


@players_bp.route('/players', methods=['POST'])
def add_player() -> Response:
    """Add a player."""
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
def fetch_player(player_id) -> str:
    """Fetch a player."""
    player = get_player(player_id)
    if not player:
        abort(404)
    return jsonify({'id': player.id, 'name': player.name, 'level': player.level})


@players_bp.route('/players/<int:player_id>', methods=['PUT'])
def modify_player(player_id) -> str:
    """Modify a player."""
    update_data = request.json
    updated_player = update_player(player_id, update_data)
    if not updated_player:
        abort(404)
    return jsonify({'id': updated_player.id, 'name': updated_player.name, 'level': updated_player.level})


@players_bp.route('/players/<int:player_id>', methods=['DELETE'])
def remove_player(player_id) -> str:
    """Remove a player."""
    player = delete_player(player_id)
    if not player:
        abort(404)
    return jsonify({'message': 'Player deleted'}), 200
