""" Handle rock-paper-scissors logic """

from enum import Enum
from typing import Optional

class RPS(Enum):
    ROCK = "R"
    PAPER = "P"
    SCISSORS = "S"

class Result(Enum):
    WIN = "W"
    LOSS = "L"
    TIE = "T"

def get_result(a: RPS, b: RPS) -> Optional[Result]:
    """ Return result of game from A's perspective 
    
    That is, if A plays ROCK and B plays SCISSORS, this function returns WIN.
    
    If given one or more invalid plays, returns None"""

    if a == b:
        return Result.TIE
    elif a == RPS.ROCK:
        if b == RPS.PAPER:
            return Result.LOSS
        elif b == RPS.SCISSORS:
            return Result.WIN
    elif a == RPS.PAPER:
        if b == RPS.ROCK:
            return Result.WIN
        elif b == RPS.SCISSORS:
            return Result.LOSS
    elif a == RPS.SCISSORS:
        if b == RPS.ROCK:
            return Result.LOSS
        if b == RPS.PAPER:
            return Result.WIN

    # unreachable if typing is adhered to
    print(f"Unknown play in match: {a} vs {b}")
    return None

def rps_from_str(s: str) -> Optional[RPS]:
    """ Validates a string into an acceptable rock-paper-scissors play. """
    s = s.lower()
    if s in ('r', 'rock', 'kivi'):
        return RPS.ROCK
    elif s in ('s', 'scissors', 'sakset'):
        return RPS.SCISSORS
    elif s in ('p', 'paper', 'paperi'):
        return RPS.PAPER
    else:
        return None

def result_from_str(s: str) -> Optional[Result]:
    """ Validates a string into an acceptable result. """
    s = s.lower()
    if s in ('w', 'win'):
        return Result.WIN
    elif s in ('l', 'loss'):
        return Result.LOSS
    elif s in ('t', 'tie'):
        return Result.TIE
    else:
        return None

# stuff for frontend templates

def is_win(res: Result) -> bool:
    """ Returns True for a winning result (i.e. Result.WIN) """
    return res is Result.WIN

def emoji_from_play(p: RPS) -> str:
    if p == RPS.ROCK:
        return "✊"
    elif p == RPS.PAPER:
        return "🖐️"
    elif p == RPS.SCISSORS:
        return "✌️"
    else:
        return ""