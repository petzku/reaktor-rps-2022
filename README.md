# Rock-Paper-Scissors Match Results

A small web-app, which displays results from rock-paper-scissors matches, catalogued by a separate API.

## Setup

Install dependencies using pip. Using `virtualenv` is recommended:
```sh
$ virtualenv venv
$ . venv/bin/activate # for sh-like shells, such as bash and zsh
$ pip install -r requirements.txt
```

Initialize the database:
```sh
$ sqlite3 app/results.db < create-database.sql
```