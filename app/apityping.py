""" Type definitions for API access """

from typing import TypedDict, Literal

RpsText = Literal['ROCK', 'PAPER', 'SCISSORS']
PlayerName = str
GameId = str
Timestamp = int

class Player(TypedDict):
    name: PlayerName

class PlayerPlay(TypedDict):
    name: PlayerName
    played: RpsText

class GameResult(TypedDict):
    type: Literal["GAME_RESULT"]
    gameId: GameId
    t: Timestamp
    playerA: PlayerPlay
    playerB: PlayerPlay

class GameBegin(TypedDict):
    type: Literal["GAME_BEGIN"]
    gameId: GameId
    playerA: Player
    playerB: Player