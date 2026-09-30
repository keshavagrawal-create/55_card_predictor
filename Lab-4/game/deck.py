import random
from game.card import Card


class Deck:

    SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
    RANKS = [
        ("2", 2), ("3", 3), ("4", 4), ("5", 5), ("6", 6),
        ("7", 7), ("8", 8), ("9", 9), ("10", 10),
        ("J", 11), ("Q", 12), ("K", 13), ("A", 14)
    ]

    def __init__(self):
        self.cards = []
        self.reset()

    def reset(self):
        self.cards = [Card(r[0], s, r[1]) for s in self.SUITS for r in self.RANKS]
        random.shuffle(self.cards)

    def draw(self):
        if not self.cards:
            self.reset()
        return self.cards.pop()

    @property
    def remaining(self):
        return len(self.cards)