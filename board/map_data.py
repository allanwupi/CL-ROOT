from board.clearing import Clearing
from board.suit import Suit

AUTUMN_MAP = [
    Clearing(0, 'The Burrow', Suit.NONE, [5,9], ['[ ]']),
    Clearing(0, 'The Burrow', Suit.NONE, [5,9], ['[ ]'])

]

# The map is rendered in two steps
# 1. Replace F,M,R with fox, mouse and rabbit color codes (N for reset)
# 2. Replace { } with building slots
AUTUMN_MAP_ASCII = r'''
                     R+-creek-+N
F+-hill--+N            R|    {} |N
F| {}    |N------------R|{}     |N___
F|       |N            R|       |N   \_____
F|       |N            R+---5---+N         \___M+-quarry+N
F+---1---+N___                               M| {}    |N
    |       \__   R+-beach-+N            ____M|       |N
    |          \__R|{}  {} |N     ______/    M|    {} |N
    |             R|       |N____/           M+---2---+N
    |             R|   {}  |N                      |
M+-dune--+N         R+--1-0--+N                      |
M|   {}  |N           /                            |
M|       |N          /          M+wtrfall+N      F+--mtn--+N
M| {}    |N_    F+-glade-+N       M|{}     |N   ___F|    {} |N
M+---9---+N \_  F|    {} |N    ___M|    {} |N__/   F|       |N
    |       \_F|       |N___/   M|{}     |N      F|{}     |N
    |         F| {}    |N       M+--1-1--+N_     F+---6---+N
    |        _F+--1-2--+N__               \_       |
    |     __/            \_               \_     |
    |    /                 \_               \    |
R+-haven-+N                    \_M+--pond-+N     \   |
R|    {} |N       F+meadow-+N      M|   {}  |N     R+-weald-+N
R|       |N___    F|   {}  |N   ___M|       |N_____R|       |N
R|{}     |N   \___F|       |N__/   M|{}     |N     R| {}    |N
R+---4---+N       F|  {}   |N      M+---7---+N     R|       |N
                F+---8---+N                    R+---3---+N
'''

def color_map(ascii: str) -> str:
    from ui.styles import Color, Style
    ascii = ascii.replace('F', Color.FOX.value)
    ascii = ascii.replace('M', Color.MOUSE.value)
    ascii = ascii.replace('R', Color.RABBIT.value)
    return ascii.replace('N', Style.RESET.value)