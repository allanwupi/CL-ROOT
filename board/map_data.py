from board.clearing import Clearing
from board.suit import Suit
from components.items import Ruin
from components.data import _ENVIRONMENT, BAG, BOOT, HAMMER, SWORD
from ui.renderer import Renderer

R1: Ruin = Ruin(owner=_ENVIRONMENT, name="R1", item=BAG)
R2: Ruin = Ruin(owner=_ENVIRONMENT, name="R1", item=BOOT)
R3: Ruin = Ruin(owner=_ENVIRONMENT, name="R1", item=HAMMER)
R4: Ruin = Ruin(owner=_ENVIRONMENT, name="R1", item=SWORD)

burrow = Clearing(0, 'Burrow', Suit.NONE, [], [None])
hill = Clearing(1, 'Hill', Suit.FOX, [5, 9, 10], [None])
quarry = Clearing(2, 'Quarry', Suit.MOUSE, [5, 6, 10], [None, None])
weald = Clearing(3, 'Weald', Suit.RABBIT, [6, 7, 11], [None])
haven = Clearing(4, 'Haven', Suit.RABBIT, [8, 9, 12], [None, None, None])
creek = Clearing(5, 'Creek', Suit.RABBIT, [1, 2], [None, None])
mountain = Clearing(6, 'Mountain', Suit.FOX, [2, 3, 11], [R1, None])
pond = Clearing(7, 'Pond', Suit.MOUSE, [3, 8, 12], [None, None])
meadow = Clearing(8, 'Meadow', Suit.FOX, [4, 7], [None, None])
dune = Clearing(9, 'Dune', Suit.MOUSE, [1, 4, 12], [None, None])
beach = Clearing(10, 'Beach', Suit.RABBIT, [1, 2, 12], [None, None, R2])
waterfall = Clearing(11, 'Waterfall', Suit.MOUSE, [3, 6, 12], [None, None, R3])
glade = Clearing(12, 'Glade', Suit.FOX, [4, 7, 9, 10, 11], [R4, None])

AUTUMN_MAP = [
    burrow,
    hill,
    quarry,
    weald,
    haven,
    creek,
    mountain,
    pond,
    meadow,
    dune,
    beach,
    waterfall,
    glade
]

# The map is rendered in two steps
# 1. Replace F,M,R with fox, mouse and rabbit color codes (N for reset)
# 2. Replace { } with building slots
AUTUMN_MAP_ASCII = r'''
                     R+-creek-+N
F+-hill--+N            R|    {creek_1}|N
F| {hill_1}   |N------------R|{creek_2}    |N___
F|       |N            R|       |N   \_____
F|       |N            R+---5---+N         \___M+-quarry+N
F+---1---+N___                               M| {quarry_1}   |N
    |       \__   R+-beach-+N            ____M|       |N
    |          \__R|{beach_1} {beach_2}|N     ______/    M|    {quarry_2}|N
    |             R|       |N____/           M+---2---+N
    |             R|   {beach_3} |N                      |
M+-dune--+N         R+--1-0--+N                      |
M|   {dune_1} |N           /                            |
M|       |N          /          M+wtrfall+N      F+--mtn--+N
M| {dune_2}   |N_    F+-glade-+N       M|{waterfall_1}    |N   ___F|    {mountain_1}|N
M+---9---+N \_  F|    {glade_1}|N    ___M|    {waterfall_2}|N__/   F|       |N
    |       \_F|       |N___/   M|{waterfall_3}    |N      F|{mountain_2}    |N
    |         F| {glade_2}   |N       M+--1-1--+N_     F+---6---+N
    |        _F+--1-2--+N__               \_       |
    |     __/            \_               \_     |
    |    /                 \_               \    |
R+-haven-+N                    \_M+--pond-+N     \   |
R|    {haven_1}|N       F+meadow-+N      M|   {pond_1} |N     R+-weald-+N
R|       |N___    F|   {meadow_1} |N   ___M|       |N_____R|       |N
R|{haven_2}    |N   \___F|       |N__/   M|{pond_2}    |N     R| {weald_1}   |N
R+---4---+N       F|  {meadow_2}  |N      M+---7---+N     R|       |N
                F+---8---+N                    R+---3---+N
'''

def color_map(ascii: str) -> str:
    from ui.styles import Color, Style
    ascii = ascii.replace('F', Color.FOX.value)
    ascii = ascii.replace('M', Color.MOUSE.value)
    ascii = ascii.replace('R', Color.RABBIT.value)
    return ascii.replace('N', Style.RESET.value)