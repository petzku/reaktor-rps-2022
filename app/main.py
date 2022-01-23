#!/usr/bin/env python3

from flask import Flask, render_template
from flask_socketio import SocketIO
import apiconn, database

from apityping import is_finished
from rps import is_win, emoji_from_play

live_games = []

def get_live_games():
    return live_games

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

    return socketio

if __name__ == "__main__":

    # update missing history
    #apiconn.fetch_new_history()

    # XXX: temporary for testing
    # live_games = database.get_games_history()

    app = create_app()
    socketio = socketio_app(app)

    socketio.run(app)