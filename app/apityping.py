""" Type definitions for API access """

from typing import TypedDict, Literal, Callable
from rps import RPS, Result

RpsText = Literal['ROCK', 'PAPER', 'SCISSORS']
PlayerName = str
PlayerId = str
GameId = str
Timestamp = int

class APIPlayer(TypedDict):
    name: PlayerName

class APIPlayerPlay(TypedDict):
    name: PlayerName
    played: RpsText

class APIGameResult(TypedDict):
    type: Literal["GAME_RESULT"]
    gameId: GameId
    t: Timestamp
    playerA: APIPlayerPlay
    playerB: APIPlayerPlay

class APIGameBegin(TypedDict):
    type: Literal["GAME_BEGIN"]
    gameId: GameId
    playerA: APIPlayer
    playerB: APIPlayer

class PlayerPlay(TypedDict):
    pid: PlayerId
    name: PlayerName
    played: RPS
    result: Result

class Player(TypedDict):
    pid: PlayerId
    name: PlayerName

class GameResult(TypedDict):
    gameId: GameId
    t: Timestamp
    player1: PlayerPlay
    player2: PlayerPlay

class GameBegin(TypedDict):
    gameId: GameId
    player1: Player
    player2: Player

ResultCallback = Callable[[GameResult], None]
BeginCallback = Callable[[GameBegin], None]

def is_finished(game: GameResult | GameBegin) -> bool:
    return 't' in game.keys()