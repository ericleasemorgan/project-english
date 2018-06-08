CREATE TABLE bibliographics (
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
	year        INT, 
	url         TEXT
);

create TABLE entities (
	eid		INT,
	entity  TEXT,
	id      TEXT,
	sid		INT,
	type    TEXT
);

create TABLE pos (
	id     TEXT,
	lemma  TEXT,
	pos    TEXT,
	sid    INT,
	tid    INT,
	token  TEXT
);

