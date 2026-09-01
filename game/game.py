from board.board import Board
from components.items import Item
from components.deck import Deck

class Game():
    def __init__(self, board: Board, deck: Deck, items: list[Item]):
        self.board = board
        self.deck = deck
        self.items: list[Item] = items # Item supply
    
    def __getitem__(self, key):
        return self.board[key]