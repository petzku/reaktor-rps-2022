PRAGMA foreign_keys = ON;

-- create "enums" for game state, rock/paper/scissors, and game result
CREATE TABLE IF NOT EXISTS status_enum (
    type        CHAR(1)     PRIMARY KEY NOT NULL,
    readable    TEXT        NOT NULL
);
INSERT INTO status_enum VALUES (0, "In progress");
INSERT INTO status_enum VALUES (1, "Finished");

CREATE TABLE IF NOT EXISTS play_enum (
    type        CHAR(1)     PRIMARY KEY NOT NULL,
    readable    TEXT        NOT NULL
);
INSERT INTO play_enum VALUES ("R", "rock");
INSERT INTO play_enum VALUES ("P", "paper");
INSERT INTO play_enum VALUES ("S", "scissors");

CREATE TABLE IF NOT EXISTS result_enum (
    type        CHAR(1)     PRIMARY KEY NOT NULL,
    readable    TEXT        NOT NULL
);
INSERT INTO result_enum VALUES ("W", "win");
INSERT INTO result_enum VALUES ("L", "loss");
INSERT INTO result_enum VALUES ("T", "tie");

-- metadata tables

CREATE TABLE IF NOT EXISTS history_page (
    id          INTEGER     PRIMARY KEY CHECK(id = 0), --enforce singleton row
    page        CHAR(12)    NULL
);
INSERT INTO history_page VALUES (0, null);

-- data tables

CREATE TABLE IF NOT EXISTS players (
    player_id   TEXT        PRIMARY KEY NOT NULL,
    name        TEXT
);

CREATE TABLE IF NOT EXISTS games (
    game_id     TEXT        PRIMARY KEY NOT NULL,
    time        DATE,
    p1_id       TEXT        NOT NULL,
    p2_id       TEXT        NOT NULL,
    status      INTEGER     NOT NULL,
    FOREIGN KEY (p1_id) REFERENCES players(player_id),
    FOREIGN KEY (p2_id) REFERENCES players(player_id),
    FOREIGN KEY (status) REFERENCES status_enum(code)
);

CREATE TABLE IF NOT EXISTS plays (
    game_id     TEXT,
    player_id   TEXT,
    played      CHAR(1)     NOT NULL,
    result      CHAR(1)     NOT NULL,
    FOREIGN KEY (played) REFERENCES play_enum(type),
    FOREIGN KEY (result) REFERENCES result_enum(type)
);