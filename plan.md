# Project plan

Rough plan, will likely be refined as I go along.

Implementation: Python, likely Flask for backend, persistent database. Front-end should be HTML + lightweight CSS/javascript.
Focus, especially in the front-end, should be on speed and responsivity.

## Front-end

At least three user-facing pages: active games, history, player statistics.
Consider also: player search, overall statistics.
- 

According to the specification, "the currently ongoing games must be visible at all times".
Websockets between client and server, with server in turn updating from API?
Think of a way to display active games on the other pages: possibly a sidebar?

Design-wise, consider also a single-page app vs. multi-page.
Latter has some benefits, including working (mostly) without javascript enabled.

## Back-end

Python + Flask + database layer. Abstract database usage, use SQLite while developing but can switch to another database (possibly even NoSQL?) for later dev/production.

Consider also being fully in-memory; likely too much data for this to be sustainable.

### API usage

Keep API `/rps/history` data mirrored in our own database to make searches faster for clients.
API does not seem to be sorted in any way.
~~Can we assume new games will always be entered at the end, and that the last cursor will always be the only one to see updates?~~
Should be unnecessary to fetch historical data except upon server startup.

Use the API's `/rps/live` websocket directly from the server. No(?) way to get status of games before the connection is opened, but this shouldn't be a major issue.
Events are either `GAME_BEGIN` or `GAME_RESULT`. Tally any incoming results in database

#### General flow

- On server initialisation, open websocket to live status updates, then start fetching historical data.
- On websocket updates:
    - Keep track in-memory of active games (`GAME_BEGIN` starts new game, `GAME_RESULT` ends it)
        - consider: keep results in-memory for a short period (30-60 seconds?)
    - Update any results into database
- On fetching historical data:
    - Update any entries into database, except where DB has a newer timestamp (i.e. received a new result from websocket after API response). Possible this may never happen.
    - Fetch next page, if one exists

### Database

- tables
    - games
        - id
        - time (timestamp of last update, from API)
        - player_1 (id)
        - player_2 (id)
        - status (in progress/result)
    - plays
        - game_id
        - player_id
        - played (rock/paper/scissors)
    - players (id-name mapping)
        - name
        - id (UUID? raw incrementing usually bad)
    - meta
        - last historical API page (kept for faster restarting of server)
