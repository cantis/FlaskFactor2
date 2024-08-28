from models import Player, get_session

def create_player(player_data):
    session = get_session()
    new_player = Player(**player_data)
    session.add(new_player)
    session.commit()
    return new_player

def get_player(player_id):
    session = get_session()
    player = session.query(Player).filter_by(id=player_id).first()
    return player

def update_player(player_id, update_data):
    session = get_session()
    player = session.query(Player).filter_by(id=player_id).first()
    if player:
        for key, value in update_data.items():
            setattr(player, key, value)
        session.commit()
    return player

def delete_player(player_id):
    session = get_session()
    player = session.query(Player).filter_by(id=player_id).first()
    if player:
        session.delete(player)
        session.commit()
    return player
