from game.game import Game, GameOver
from board.board import Board
from board.map_data import AUTUMN_MAP_ASCII, AUTUMN_MAP
from components.deck import Deck
from components.data import BASE_DECK
from ui.styles import Color
from factions.clockwork.marquise import MechanicalMarquise
import copy


def get_data() -> list:
    board: Board = Board(clearings=copy.deepcopy(AUTUMN_MAP), ascii=AUTUMN_MAP_ASCII)
    deck: Deck = Deck(name="Base Deck", cards=BASE_DECK)
    game: Game = Game(board=board, deck=deck, pause_each_phase=False)
    bot1 = MechanicalMarquise(name='Marquise')
    bot2 = MechanicalMarquise(name='Esiuqram', color=Color.PINK)
    game.setup(bot1)
    game.setup(bot2)
    while True:
        try:
            game.play()
        except GameOver as e:
            return game.vp_history
    
def main(N: int = 100):
    with open('log.txt', 'a') as f:
        for i in range(N):
            vp = get_data()
            f.write(f"{vp}\n")

if __name__ == "__main__":
    main()