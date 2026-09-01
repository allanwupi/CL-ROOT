from game.game import Game, GameOver
from board.board import Board
from board.map_data import AUTUMN_MAP, AUTUMN_MAP_ASCII
from components.deck import Deck
from components.card_data import BASE_DECK
from ui.styles import Color
from ui.cli import CLI
from factions.clockwork.marquise import MechanicalMarquise

board: Board = Board(clearings=AUTUMN_MAP, ascii=AUTUMN_MAP_ASCII)
deck: Deck = Deck(name="Base Deck", cards=BASE_DECK)
game: Game = Game(board=board, deck=deck)

bot1 = MechanicalMarquise(name='Marquise')
bot2 = MechanicalMarquise(name='Esiuqram', color=Color.PINK)

cli: CLI = CLI(game)

def main_loop():
    print()
    game.setup(bot1)
    game.setup(bot2)
    
    try:
        cli.main_loop()
    except KeyboardInterrupt as e:
        print()
        return()
    except GameOver as e:
        print(e)
        print(game)  # Show final board state