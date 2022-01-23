""" Database abstraction layer """

import sqlite3
from uuid import uuid4
import rps

from typing import Optional
from apityping import GameResult


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

def _add_game_result(gid: str, time: int, p1_id: str, p2_id: str, p1_play: rps.RPS, p2_play: rps.RPS) -> bool:
    """ Add a result to the database
    
    Returns True if successful, False if not."""

    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    result_query = "INSERT INTO games(game_id,time,p1_id,p2_id,status) VALUES (?,?,?,?,?)"
    play_query = "INSERT INTO plays(game_id,player_id,played,result) VALUES (?,?,?,?)"

    try:
        cur.execute(result_query, (gid, time, p1_id, p2_id, 1)) # 1 = finished
        
        p1_res = rps.get_result(p1_play, p2_play)
        p2_res = rps.get_result(p2_play, p1_play)
        assert (p1_res is not None) and (p2_res is not None)

        cur.executemany(play_query, (
            (gid, p1_id, p1_play.value, p1_res.value),
            (gid, p2_id, p2_play.value, p2_res.value)
        ))

        con.commit()
        return True
    except sqlite3.Error as e:
        print("Database error: ", e)
        return False
    finally:
        con.close()

def add_history_games(data: list[GameResult]) -> None: # TODO: typing
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
    for game in data:
        gid = game['gameId']
        t = game['t']
        p1, p2 = game['playerA'], game['playerB']

        p1_id = ids[p1['name']]
        p1_play = rps.rps_from_str(p1['played'])
        
        p2_id = ids[p2['name']]
        p2_play = rps.rps_from_str(p2['played'])

        assert (p1_play is not None) and (p2_play is not None)

        if not _add_game_result(gid, t, p1_id, p2_id, p1_play, p2_play):
            print("Error adding game: ", game)
