#!/usr/bin/env bash

# assert.sh - given a lemmatized noun and verb, list frequencies of assertions and negations

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame and distributed under a GNU Public License

# June 11, 2018 - first cut, and thanks to go Don Brower


# configure
DB='sqlite3 ./etc/carrell.db'
HEADER=".mode tabs\n"

# sanity check
if [[ -z $1 ]]; then
	echo "Usage: $0 <lemmatized noun> <lemmatized verb>"
	exit
fi

QUERY="SELECT COUNT ( LOWER( t.token || ' ' || c.token || ' ' || d.token ) ) AS frequency , ( LOWER( t.token || ' ' || c.token || ' ' || d.token ) ) AS sentence
FROM pos AS t
JOIN pos AS c
ON c.tid=t.tid+1 AND c.sid=t.sid AND c.id=t.id
JOIN pos AS d
ON d.tid=t.tid+2 AND d.sid=t.sid AND d.id=t.id
WHERE t.lemma IS '$1'
AND c.lemma IS '$2'
AND ( d.pos LIKE 'N%' OR d.pos LIKE 'J%' )
GROUP BY ( LOWER( t.token || ' ' || c.token || ' ' || d.token ) )
ORDER BY frequency DESC, ( LOWER( t.token || ' ' || c.token || ' ' || d.token ) ) ASC;"

# set up, debug, do the work, and done
echo "Assertions regarding $1 $2"
echo -e "$HEADER$QUERY" | $DB
echo

QUERY="SELECT COUNT( LOWER( t.token || ' ' || c.token || ' ' || d.token || ' ' || e.token ) ) AS frequency, ( LOWER( t.token || ' ' || c.token || ' ' || d.token || ' ' || e.token ) ) AS sentence
FROM pos AS t
JOIN pos AS c
ON c.tid=t.tid+1 AND c.sid=t.sid AND c.id=t.id
JOIN pos AS d
ON d.tid=t.tid+2 AND d.sid=t.sid AND d.id=t.id
JOIN pos AS e
ON e.tid=t.tid+3 AND e.sid=t.sid AND e.id=t.id
WHERE t.lemma IS '$1'
AND c.lemma IS '$2'
AND ( d.token IS 'no' OR d.token IS 'not' )
AND ( e.pos LIKE 'N%' OR e.pos LIKE 'J%' )
GROUP BY LOWER( t.token || ' ' || c.token || ' ' || d.token || ' ' || e.token )
ORDER BY frequency DESC, ( LOWER( t.token || ' ' || c.token || ' ' || d.token || ' ' || e.token ) ) ASC;"

# set up, debug, do the work, and done
echo "Negations regarding $1 $2"
echo -e "$HEADER$QUERY" | $DB




