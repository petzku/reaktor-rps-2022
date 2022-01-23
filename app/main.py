#!/usr/bin/env python3

from flask import Flask, render_template
from flask_socketio import SocketIO
import apiconn

from apityping import is_finished
from rps import is_win


def create_app():
    app = Flask(__name__)

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
        # TODO
        return f"player {pid}"
    return app

def socketio_app(app):
    socketio = SocketIO(app)

    return socketio

if __name__ == "__main__":

    # update missing history
    #apiconn.fetch_new_history()

    app = create_app()
    socketio = socketio_app(app)

    socketio.run(app)