from components.card import Card
from card_data import *
from random import shuffle

class Deck:
    def __init__(self, name: str, cards: list[Card]):
        self.name: str = name
        self.draw_pile: list[Card] = cards[:]
        shuffle(self.draw_pile)
        self.discard_pile: list[Card] = []
    
    def draw(self, numcards: int = 1) -> list[Card]:
        drawn: list[Card] = []
        for i in range(numcards):
            if len(self.draw_pile) == 0:
                print(f"The discard pile was reshuffled to form a new deck.")
                self.reshuffle()
            drawn.append(self.draw_pile.pop())
        return drawn
    
    def add(self, cards: list[Card]) -> None:
        self.draw_pile.extend(cards)
        
    def discard(self, cards: list[Card]) -> None:
        self.discard_pile.extend(cards)
    
    def reshuffle(self) -> None:
        self.draw_pile.extend(self.discard_pile)
        self.draw_pile = []
        shuffle(self.draw_pile)