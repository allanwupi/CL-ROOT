from random import shuffle

from components.card import Card
from components.data import *

class Deck:
    def __init__(self, name: str, cards: list[Card]):
        self.name: str = name
        self.size = len(cards)
        self.draw_pile: list[Card] = cards[:]
        shuffle(self.draw_pile)
        self.discard_pile: list[Card] = []
        
    def __len__(self) -> int:
        return self.size
    
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
        
    def discard(self, pile: list[Card], card: Card)-> None:
        pile.remove(card)
        self.discard_pile.append(card)
    
    def reshuffle(self) -> None:
        self.draw_pile.extend(self.discard_pile)
        self.draw_pile = []
        shuffle(self.draw_pile)