# Rock-Paper-Scissors Match Results

A small web-app, which displays results from rock-paper-scissors matches, catalogued by a separate API.

## Setup

Requires Python 3.10 or greater.

Install dependencies using pip. Using `virtualenv` is recommended:
```sh
$ virtualenv venv
$ . venv/bin/activate # for sh-like shells, such as bash and zsh
(venv) $ pip install -r requirements.txt
```

Initialize the database:
```sh
$ sqlite3 app/results.db < create-database.sql
```

## Running

For local testing, simply run the `main.py` script inside the `app/` directory. Optionally, set `FLASK_ENV` to `development` to enable most logging:

```sh
(venv) $ cd app
(venv) $ export FLASK_ENV=development
(venv) $ python3 main.py
```