import random

from utils import DiggingError, Card, Turn, Fight


import dummy
player_classes = [dummy.DummyPlayerOne, dummy.DummyPlayerTwo]


def create_players():
    """
    """
    random.shuffle(player_classes)
    players = []
    for i in range(4):
        try:
            player = player_classes[i % 2]()
        except:
            raise DiggingError('Error while creating a player from class %s' % str(player_classes[i % 2]))
        else:
            players.append(player)
    for player in players:
        try:
            player.look_around(players)
        except:
            raise DiggingError('Error when calling look_around() on player %s' % str(player))
    return players


def create_talon():
    """
    """
    talon = []
    for i in range(3):
        talon.append(Card('mine', 'gold'))
        talon.append(Card('mine', 'silver'))
        talon.append(Card('mine', 'copper'))
    for i in range(9):
        talon.append(Card('closer'))
    for i in range(1, 13):
        talon.append(Card('bandit', i))
    for i in range(9):
        talon.append(Card('gold_coffer', 1))
        talon.append(Card('silver_coffer', 1))
        talon.append(Card('copper_coffer', 1))
    talon.append(Card('gold_coffer', 2))
    talon.append(Card('silver_coffer', 2))
    talon.append(Card('copper_coffer', 2))
    random.shuffle(talon)
    return talon


def inform_players(players, player, turn):
    """
    """
    for informed_player in players:
        try:
            informed_player.tell_info(player, turn)
        except:
            raise DiggingError('Error when calling tell_info() on player %s' % str(player))


def print_result():
    """
    """
    print('Ende')


def main():
    """
    """
    # Check player classes setup
    assert len(player_classes) == 2

    # Create player and card instances
    players = create_players()
    talon = create_talon()

    # Give 6 cards to each player
    for i in range(6):
        for player in players:
            try:
                player.get_card(card=talon.pop(), origin='talon')
            except:
                raise DiggingError('Error when calling get_card() on player %s' % str(player))

    # Run the game
    open_mines = []
    remaining_turns = None
    fight = None
    while True:
        for player in players:
            # Check if we are in the last round
            if remaining_turns is not None:
                if remaining_turns == 0:
                    break
                else:
                    remaining_turns += -1

            # One player's turn
            try:
                turn = player.your_turn()
            except:
                raise DiggingError('Error when calling your_turn() on player %s' % str(player))
            else:
                assert isinstance(turn, Turn)

                # Process the turn
                if turn.category == 'pass':
                    if remaining_turns is None:
                        raise DiggingError('Player %s tries to pass but there are still cards on talon.' % str(player))
                    inform_players(players, player, Turn(category='pass'))

                if turn.category == 'draw':
                    if talon:
                        player.get_card(card=talon.pop(), origin='talon')
                        inform_players(players, player, Turn(category='draw'))
                        if not talon:
                            remaining_turns = 4
                    else:
                        raise DiggingError('Player %s tries to draw a card from empty talon.' % str(player))

                if turn.category == 'shift':
                    players[(player.seat + 2) % 4].get_card(card=turn.card, origin='mate')
                    inform_players(player, Turn(category='shift'))

                if turn.category == 'play':
                    if turn.card.category == 'mine':
                        open_mines.append((turn.card, turn.target))

                    if turn.card.category == 'bandit':
                        if fight:
                            if (fight.attacker.seat + 2) % 4 == player.seat:
                                fight.add_bandit(turn.card)
                            else:
                                fight.add_bandit(turn.card, defense=True)
                            if (fight.attacker.seat + 3) % 4 == player.seat:
                                if fight.successful:
                                    pass
                                    # fight.attacker.get_new_mine(fight.card)
                                    # TODO: Move mine from defender to attacker
                                fight = None
                        else:
                            fight = Fight(card=turn.target, attacker=player)
                            fight.add_bandit(turn.card, defense=False)

                    if turn.card.category == 'closer':
                        if fight and fight.card == turn.target:
                            # TODO Pop last item of the mine
                            fight = None
                        # TODO Close mine and score player

                    if turn.card.category in ['gold_coffer', 'silver_coffer', 'copper_coffer']:
                        pass
                        # TODO Put item as last item into mine
                    inform_players(player, Turn(category=turn.category, target=turn.target))
        else:
            continue
        break
    print_result()
    return 0


if __name__ == '__main__':
    main()
