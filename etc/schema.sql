CREATE TABLE titles (
  century     INT,
  city        TEXT,
  collection  TEXT,
  date        TEXT,
  extent      TEXT,
  id          TEXT PRIMARY KEY,
  imprint     TEXT,
  language    TEXT,
  pages       INT,
  place       TEXT,
  publisher   TEXT,
  title       TEXT,
  words       INT,
  year        INT
);

create TABLE authors (
  collection  TEXT,
  id          TEXT,
  author      TEXT	
);