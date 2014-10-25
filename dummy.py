from utils import Turn


class DummyPlayerOne():
    """
    """
    def __init__(self):
        self.cards = set()
        self.all_talon_cards = 36

    def look_around(self, players):
        self.players = players

    def get_card(self, card, origin):
        self.cards.add(card)

    def your_turn(self):
        if self.all_talon_cards:
            turn = Turn(category='draw')
        else:
            turn = Turn(category='pass')
        return turn

    def tell_info(self, player, turn):
        if turn.category == 'draw':
            self.all_talon_cards += -1


class DummyPlayerTwo(DummyPlayerOne):
    pass
