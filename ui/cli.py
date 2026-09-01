from game.game import Game, GameOver
from board.board import Board
from board.suit import Suit
from factions.clockwork.marquise import MechanicalMarquise

# board: Board = Board(clearings=AUTUMN_MAP, ascii=AUTUMN_MAP_ASCII)
# bot1 = MechanicalMarquise(name='Marquise')
# bot2 = MechanicalMarquise(name='Esiuqram', ansi_color='\033[38;5;183m')

CONTINUE_COMMANDS = [ 'yes', 'y', 'continue', 'c', 'play', 'p', 'run', 'r', 'next']
TERMINATE_COMMANDS = ['no', 'n', 'quit', 'q', 'exit', 'x', 'end', 'e', 'stop']
DISPLAY_COMMANDS = ['map', 'm', 'display', 'd', 'board', 'b', 'view', 'v']
HELP_COMMANDS = ['?', 'help', 'h', 'info', 'i', 'manual', 'man']
# CLEARING_VIEWS = {str(i) for i in range(1,board.size)}
SUIT_VIEWS = {'bunny': Suit.RABBIT, 'rabbit': Suit.RABBIT, 'fox': Suit.FOX, 'mouse': Suit.MOUSE, 'wild': Suit.WILD}
NAMED_CLEARINGS = {
    'hill': 1,
    'quarry': 2,
    'weald': 3,
    'haven': 4,
    'creek': 5,
    'mountain': 6,
    'pond': 7,
    'meadow': 8,
    'dune': 9,
    'beach': 10,
    'waterfall': 11,
    'glade': 12
}
EXECUTION_SYMBOLS = ['!', '/']

USAGE_PROMPT: str = f"""usage:
  - continue      : (y)es  | (c)ontinue | (p)lay   | (r)un  | next | <ENTER>
  - exit program  : (n)o   | (q)uit     | e(x)it   | (e)nd  | stop | <CTRL-C>
  - view clearing : [1-12] | rabbit     | bunny    | mouse  | fox  | wild
  - view board    : (v)iew | (d)isplay  | (b)oard  | (m)ap
  - show help     : (h)elp | (man)ual   | (i)nfo   | ?
  - execute code  : \033[1m!\033[0mcode  | \033[1m/\033[0mcode
"""

# def main_loop():
#     print()
#     board.setup(bot1)
#     board.setup(bot2)
#     print(f'Setup complete. Press \033[1m<ENTER>\033[0m to continue.\n')
#     print(board)
#     try:
#         while True:
#             command_sequence: str = input('\033[2m>\033[0m ')
#             if not command_sequence:
#                 board.play()
#             elif command_sequence[0] in EXECUTION_SYMBOLS:
#                 try:
#                     exec(command_sequence[1:])
#                     continue
#                 except Exception as e:
#                     print(f'\033[31m{repr(e)}\033[0m')
#             tokens: list[str] = command_sequence.split()
#             for command in tokens:
#                 if command.lower() in CONTINUE_COMMANDS:
#                     board.play()
#                 elif command.lower() in DISPLAY_COMMANDS:
#                     print(board)
#                 elif command in NAMED_CLEARINGS:
#                     print(board[NAMED_CLEARINGS[command]])
#                 elif command in CLEARING_VIEWS:
#                     print(board[int(command)])
#                 elif command.lower() in SUIT_VIEWS:
#                     suit: Suit = SUIT_VIEWS[command.lower()]
#                     clearings: list[int] = [i for i in range(1,board.size) if board[i].suit in suit]
#                     for clearing in clearings:
#                         print(board[clearing])
#                 elif command.lower() in TERMINATE_COMMANDS:
#                     raise GameOver("Game was terminated.")
#                 else:
#                     print(USAGE_PROMPT)
#                     break
#     except KeyboardInterrupt as e:
#         print()
#         return()
#     except GameOver as e:
#         print(e)
#         print(board)  # Show final board state