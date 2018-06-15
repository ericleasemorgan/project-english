-- carrel.sql - the schema for a subcollection ("study carrel") of Project English

-- Eric Lease Morgan <emorgan@nd.edu>
-- June 8, 2018 - first cut and while attending ELAG 2018


-- authors
create TABLE authors (
	collection TEXT,
	id         TEXT,
	author     TEXT
);

-- titles
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

-- named entities
CREATE TABLE entities (
	eid    INT,
	entity TEXT,
	id     TEXT,
	sid    INT,
	type   TEXT 
);

-- parts-of-speech
CREATE TABLE pos (
	id    TEXT,
	lemma TEXT,
	pos   TEXT,
	sid   INT,
	tid   INT,
	token TEXT
);
