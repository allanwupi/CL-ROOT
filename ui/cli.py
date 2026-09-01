from game.game import Game, GameOver
from ui.renderer import Renderer
from ui.styles import Style, Color
from board.suit import Suit


class CLI:
    CONTINUE_COMMANDS = [ "yes", "y", "continue", "c", "play", "p", "run", "r", "next"]
    TERMINATE_COMMANDS = ["no", "n", "quit", "q", "exit", "x", "end", "e", "stop"]
    DISPLAY_COMMANDS = ["map", "m", "display", "d", "board", "b", "view", "v"]
    HELP_COMMANDS = ["?", "help", "h", "info", "i", "manual", "man"]
    EXECUTION_COMMANDS = ["!", "/"]
    SUIT_VIEWS = {"bunny": Suit.RABBIT, "rabbit": Suit.RABBIT, "fox": Suit.FOX, "mouse": Suit.MOUSE, "wild": Suit.WILD}
    
    USAGE_PROMPT: str = f"""usage:
    - continue      : (y)es  | (c)ontinue | (p)lay   | (r)un  | next | <ENTER>
    - exit program  : (n)o   | (q)uit     | e(x)it   | (e)nd  | stop | <CTRL-C>
    - view clearing : [1-12] | rabbit     | bunny    | mouse  | fox  | wild
    - view board    : (v)iew | (d)isplay  | (b)oard  | (m)ap
    - show help     : (h)elp | (man)ual   | (i)nfo   | ?
    - execute code  : \x1b[1m!\x1b[0mcode  | \x1b[1m/\x1b[0mcode
    """

    def __init__(self, game: Game):
        self.game: Game = game
        self.size: int = len(game.board)
        self.CLEARING_VIEWS: set[str] = {str(i) for i in range(1,self.size)}
        self.NAMED_CLEARINGS: dict[str, int] = {
            "hill": 1,
            "quarry": 2,
            "weald": 3,
            "haven": 4,
            "creek": 5,
            "mountain": 6,
            "pond": 7,
            "meadow": 8,
            "dune": 9,
            "beach": 10,
            "waterfall": 11,
            "glade": 12
        }
    
    def render(self):
        print(Renderer.render_game(self.game))

    def main_loop(self):
        print(f"Setup complete. Press {Style.BOLD.style('<ENTER>')} to continue.\n")
        Renderer.render_game(self.game)
        while True:
            command_sequence: str = input(f"{Style.DIM.style('>')} ")
            if not command_sequence:
                self.game.play()
            elif command_sequence[0] in self.EXECUTION_COMMANDS:
                try:
                    exec(command_sequence[1:])
                    continue
                except Exception as e:
                    print(f"{Color.ERROR.style(repr(e))}")
            tokens: list[str] = command_sequence.split()
            for command in tokens:
                if command.lower() in self.CONTINUE_COMMANDS:
                    self.game.play()
                elif command.lower() in self.DISPLAY_COMMANDS:
                    print(Renderer.render_game(self.game))
                elif command.lower() in self.NAMED_CLEARINGS:
                    print(Renderer.render_clearing(self.game, self.NAMED_CLEARINGS[command.lower()]))
                elif command in self.CLEARING_VIEWS:
                    print(Renderer.render_clearing(self.game, int(command)))
                elif command.lower() in self.SUIT_VIEWS:
                    suit: Suit = self.SUIT_VIEWS[command.lower()]
                    clearing_numbers: list[int] = [i for i in range(1,self.size) if self.game[i].suit in suit]
                    for number in clearing_numbers:
                        print(Renderer.render_clearing(self.game, number))
                elif command.lower() in self.TERMINATE_COMMANDS:
                    raise GameOver("Game was terminated.")
                else:
                    print(self.USAGE_PROMPT)
                    break