from enum import Enum
from colorama import Fore, Back, Style, init

init(autoreset=True)  # Ensures colors reset after each print

class Colour(Enum):
    # Foreground text colors
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    CYAN = Fore.CYAN
    MAGENTA = Fore.MAGENTA
    WHITE = Fore.WHITE
    BLACK = Fore.BLACK

    # Background colors
    BG_RED = Back.RED
    BG_GREEN = Back.GREEN
    BG_YELLOW = Back.YELLOW
    BG_BLUE = Back.BLUE
    BG_CYAN = Back.CYAN
    BG_MAGENTA = Back.MAGENTA
    BG_WHITE = Back.WHITE
    BG_BLACK = Back.BLACK

    # Style modifiers
    BRIGHT = Style.BRIGHT
    DIM = Style.DIM
    NORMAL = Style.NORMAL
    RESET = Style.RESET_ALL

