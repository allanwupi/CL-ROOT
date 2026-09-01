from board.clearing import Clearing
from board.suit import Suit
from ui.renderer import Renderer

burrow = Clearing(0, 'Burrow', Suit.NONE, [5,9], [None])
hill = Clearing(1, 'Hill', Suit.FOX, [5,9], [None])
quarry = Clearing(2, 'Quarry', Suit.MOUSE, [5,6,10], [None, None])

AUTUMN_MAP = [
    burrow,
    hill,
]

# The map is rendered in two steps
# 1. Replace F,M,R with fox, mouse and rabbit color codes (N for reset)
# 2. Replace { } with building slots
AUTUMN_MAP_ASCII = r'''
                     R+-creek-+N
F+-hill--+N            R|    {creek_1} |N
F| {hill_1}    |N------------R|{creek_2}     |N___
F|       |N            R|       |N   \_____
F|       |N            R+---5---+N         \___M+-quarry+N
F+---1---+N___                               M| {quarry_1}    |N
    |       \__   R+-beach-+N            ____M|       |N
    |          \__R|{beach_1}  {beach_2} |N     ______/    M|    {quarry_2} |N
    |             R|       |N____/           M+---2---+N
    |             R|   {beach_3}  |N                      |
M+-dune--+N         R+--1-0--+N                      |
M|   {dune_1}  |N           /                            |
M|       |N          /          M+wtrfall+N      F+--mtn--+N
M| {dune_2}    |N_    F+-glade-+N       M|{wtrfall_1}     |N   ___F|    {mtn_1} |N
M+---9---+N \_  F|    {glade_1} |N    ___M|    {wtrfall_2} |N__/   F|       |N
    |       \_F|       |N___/   M|{wtrfall_3}     |N      F|{mtn_2}     |N
    |         F| {glade_2}    |N       M+--1-1--+N_     F+---6---+N
    |        _F+--1-2--+N__               \_       |
    |     __/            \_               \_     |
    |    /                 \_               \    |
R+-haven-+N                    \_M+--pond-+N     \   |
R|    {haven_1} |N       F+meadow-+N      M|   {pond_1}  |N     R+-weald-+N
R|       |N___    F|   {meadow_1}  |N   ___M|       |N_____R|       |N
R|{haven_2}     |N   \___F|       |N__/   M|{pond_2}     |N     R| {weald_1}    |N
R+---4---+N       F|  {meadow_2}   |N      M+---7---+N     R|       |N
                F+---8---+N                    R+---3---+N
'''

def color_map(ascii: str) -> str:
    from ui.styles import Color, Style
    ascii = ascii.replace('F', Color.FOX.value)
    ascii = ascii.replace('M', Color.MOUSE.value)
    ascii = ascii.replace('R', Color.RABBIT.value)
    return ascii.replace('N', Style.RESET.value)