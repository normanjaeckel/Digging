class DiggingError(Exception):
    """
    """
    pass


class Card():
    """
    """
    def __init__(self, category, value=None):
        self.category = category
        self.value = value


class Turn():
    """
    """
    def __init__(self, category, target=None):
        self.category = category
        if target:
            self.target = target


class Fight():
    """
    """
    def __init__(self, card, player):
        self.card = card
        self.attacker = player
        self.attacker_bandits = []
        self.defender_bandits = []

    def add_bandit(self, card, defense=False):
        if defense:
            self.defender_bandits.append(card)
        else:
            self.attacker_bandits.append(card)

    def successful(self):
        if sum([bandit.value for bandit in self.attacker_bandits]) > sum([bandit.value for bandit in self.defender_bandits]):
            result = True
        else:
            result = False
        return result
