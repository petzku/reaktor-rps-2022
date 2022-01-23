#!/usr/bin/env python3

from flask import Flask, render_template
from flask_socketio import SocketIO
import apiconn, database
import threading

from apityping import GameBegin, GameResult, is_finished
from rps import is_win, emoji_from_play

live_games = {}

class ApiListenerThread(threading.Thread):
    def __init__(self, startup):
        threading.Thread.__init__(self)
        self.runnable = startup

    def run(self):
        self.runnable()

def get_live_games():
    return live_games.values()

def create_app():
    app = Flask(__name__)

    app.jinja_env.globals.update(
        live_games = get_live_games,
        is_finished = is_finished,
        is_win = is_win,
        emoji = emoji_from_play
    )

    @app.route("/")
    def live():
        # TODO
        return render_template("live.html")

    @app.route("/history")
    def history():
        # TODO
        return "history"

    @app.route("/player/")
    def player_search():
        # TODO
        return "player_search"

    @app.route("/player/<uuid:pid>")
    def player(pid: str):
        pid = str(pid)
        _player = database.get_player(pid)

        ((w,l,t), plays) = database.get_player_stats(pid)

        most_played_count = max(plays)
        most_played = ("Rock", "Paper", "Scissors")[plays.index(most_played_count)]

        past_games = database.get_games_by_player(pid)

        return render_template("player.html",
            player = _player,
            wins = w, losses = l, ties = t, games = (w+l+t),
            most_played = most_played, most_played_count = most_played_count,
            past_games = past_games
        )
    return app

def socketio_app(app):
    socketio = SocketIO(app)

    def on_api_gamebegin(game: GameBegin) -> None:
        # new game, add to live games and broadcast
        live_games[game['gameId']] = game

        socketio.emit('game_begin', {'gameInfo': game}, namespace='/livefeed')

    def on_api_gameresult(game: GameResult) -> None:
        # game finished, remove from live games (if it is there)
        live_games.pop(game['gameId'], None)

        socketio.emit('game_result', {'gameId': game['gameId']}, namespace='/livefeed')

    api_listener = apiconn.create_websocket_listener(on_api_gameresult, on_api_gamebegin)

    return socketio, api_listener

if __name__ == "__main__":

    # update missing history
    #apiconn.fetch_new_history()

    # XXX: temporary for testing
    # live_games = database.get_games_history()

    app = create_app()
    socketio, api_ws = socketio_app(app)

    api_thread = ApiListenerThread(api_ws.run_forever)
    api_thread.start()

    socketio.run(app)