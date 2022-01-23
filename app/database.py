""" Database abstraction layer """

import sqlite3
from uuid import uuid4
import rps

from typing import Optional
from apityping import APIGameResult, GameResult


DB_FILE = 'results.db'

def get_last_history_page() -> Optional[str]:
    """ Returns latest unfetched history page address """
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    cur.execute("SELECT page FROM history_page")
    res = cur.fetchone()
    con.close()

    # Query should always return something, as the database is initialized with a NULL page.
    # Nevertheless, check both that a row is returned and that the row has a page.
    # If yes, return it; otherwise return None
    if res:
        page, = res
        if page:
            return page
    return None

def update_history_page(key: str) -> None:
    """ Stores the cursor address for the history API endpoint """
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    try:
        cur.execute("UPDATE history_page SET page=?;", (key,))
        con.commit()
    except sqlite3.Error as e:
        print("Database error: ", e)
    con.close()

def _get_player_ids_by_name(names: list[str]) -> dict[str, str]:
    """ Get ids for players in the given list, assuming they are in the database """
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    query = "SELECT name,player_id FROM players WHERE name in ({})".format(','.join("?" for name in names))
    cur.execute(query, names)

    res = cur.fetchall()
    con.close()

    return {name: id for name,id in res}

def _create_player(name: str, uuid: str) -> bool:
    """ Add a new player to the database 
    
    Returns True if successful, False if player could not be added."""

    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    try:
        cur.execute("INSERT INTO players(name,player_id) VALUES (?,?)", (name,uuid))
        con.commit()
        return True
    except sqlite3.Error as e:
        print("Database error: ", e)
        return False
    finally:
        con.close()

def add_game_result(game: GameResult) -> bool:
    """ Add a result to the database
    
    Returns True if successful, False if not."""

    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    result_query = "INSERT INTO games(game_id,time,p1_id,p2_id,status) VALUES (?,?,?,?,?)"
    play_query = "INSERT INTO plays(game_id,player_id,played,result) VALUES (?,?,?,?)"

    p1 = game['player1']
    p2 = game['player2']

    try:
        cur.execute(result_query, (game['gid'], game['time'], p1['pid'], p2['pid'], 1)) # 1 = finished
        
        cur.executemany(play_query, (
            (gid, p1['pid'], p1['played'].value, p1['result'].value),
            (gid, p2['pid'], p2['played'].value, p2['result'].value)
        ))

        con.commit()
        return True
    except sqlite3.Error as e:
        print("Database error: ", e)
        return False
    finally:
        con.close()

def add_history_games(data: list[APIGameResult]) -> None: # TODO: typing
    """ Add one or more game results to the database """

    # Start by getting existing player IDs from database
    players = set()
    for game in data:
        p1_name = game['playerA']['name']
        p2_name = game['playerB']['name']
        players |= {p1_name, p2_name}
    ids = _get_player_ids_by_name(list(players))

    # If some players aren't in database yet, add them
    for player in players:
        if player not in ids:
            uuid = str(uuid4())
            if _create_player(player, uuid):
                ids[player] = uuid
            else:
                print(f"Error adding player '{player}' with ID {uuid}.")

    # Preprocess results into nicer data format and save to database
    for api_res in data:
        res = result_from_api_result(api_res)
        if not add_game_result(res):
            print("Error adding game: ", game)


def result_from_api_result(api_res: APIGameResult) -> GameResult:
    p1, p2 = api_res['playerA'], api_res['playerB']

    ids = _get_player_ids_by_name([p1['name'], p2['name']])

    p1_id = ids[p1['name']]
    p1_play = rps.rps_from_str(p1['played'])

    p2_id = ids[p2['name']]
    p2_play = rps.rps_from_str(p2['played'])

    assert (p1_play is not None) and (p2_play is not None)

    p1_res = rps.get_result(p1_play, p2_play)
    p2_res = rps.get_result(p2_play, p1_play)
    assert (p1_res is not None) and (p2_res is not None)

    return {
        'gameId': api_res['gameId'],
        't': api_res['t'],
        'player1': {
            'pid': p1_id,
            'name': p1['name'],
            'played': p1_play,
            'result': p1_res
        },
        'player2': {
            'pid': p2_id,
            'name': p2['name'],
            'played': p2_play,
            'result': p2_res
        }
    }
