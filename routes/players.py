"""Player Routes."""
from flask import Blueprint, render_template

from services.players_service import create_player, delete_player, get_player, update_player

players_bp = Blueprint('players', __name__, template_folder='templates')

@players_bp.route('/')
def index() -> str:
    """Players home page."""
    return render_template('players.html')

@players_bp.route('/players', methods=['POST'])
def add_player() -> str:
    """Add a player."""
    player_data = request.json
    new_player = create_player(player_data)
    return jsonify({'id': new_player.id, 'name': new_player.name, 'level': new_player.level}), 201

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
