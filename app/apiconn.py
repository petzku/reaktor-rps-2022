""" Connects to the API and fetches game data. """

import database
import requests
from typing import Optional, TypedDict, Literal


API_BASE = "https://bad-api-assignment.reaktor.com/rps"

## Type definitions
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


def _fetch_history_page(key: Optional[str] = None) -> tuple[Optional[str], list[GameResult]]:
    """ Fetch single page from the API
    
    key:
        Either string of the "cursor" address from last API access,
        or None if this is the first time accessing the API.
    
    returns (nextpage, data)
    nextpage:
        string of the next "cursor" address, or None if this was the last page.
    data:
        raw, untouched JSON from the API. Structured as a list of GameResult dicts:
        {
            "type": "GAME_RESULT",
            "gameId": string,
            "t": timestamp,
            "playerA": {"name": string, "played": RpsText},
            "playerB": {"name": string, "played": RpsText}
        }
        RpsText is one of "ROCK", "PAPER", "SCISSORS".
    """
    if key:
        url = API_BASE + "/history?cursor=" + key
    else:
        url = API_BASE + "/history"

    res = requests.get(url).json()
    page, data = res['cursor'], res['data']
    if page:
        page = page.split("=")[1]
    return page, data

def fetch_new_history() -> None:
    key = database.get_last_history_page()
    while True:
        nextkey, data = _fetch_history_page(key)
        # Either `nextkey` has the cursor for the next history page, or we've reached the last page.
        # In the latter case, `data` will also be empty.
        if nextkey:
            key = nextkey
            database.add_history_games(data)

            # save newest "page" URL to DB whenever we finish processing the page
            database.update_history_page(key)
