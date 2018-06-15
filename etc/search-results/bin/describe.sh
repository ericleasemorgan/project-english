#!/usr/bin/env bash

# describe.sh - given a lemma, list the lemmatized adjectives immediately preceding it

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame and distributed under a GNU Public License

# January 3, 2018 - first cut; "Thanks go to Sean Summers for the JOIN operation!"
# June    6, 2018 - put into Project English


# configure
DB='sqlite3 ./etc/carrell.db'
HEADER=".mode tabs\n"

# sanity check
if [[ -z $1 ]]; then
	echo "Usage: $0 <lemmatized noun>"
	exit
fi

QUERY="SELECT COUNT( LOWER( c.token || ' ' || t.token ) ) AS frequency, ( LOWER( t.token || ' ' || c.token ) ) AS phrase
FROM pos AS t
JOIN pos AS c
ON c.tid=t.tid+1 AND c.sid=t.sid AND c.id=t.id
WHERE t.pos LIKE 'J%'
AND c.lemma='$1'
GROUP BY LOWER( t.token || ' ' || c.token )
ORDER BY frequency DESC, LOWER( t.token || ' ' || c.token ) ASC;"

# set up, debug, do the work, and done
echo "Positive descriptions of $1"
echo -e "$HEADER$QUERY" | $DB
echo

QUERY="SELECT COUNT(t.token) AS frequency, ( LOWER( d.token || ' ' || t.token || ' ' || c.token ) ) AS phrase
FROM pos AS t
JOIN pos AS c
ON c.tid=t.tid+1 AND c.sid=t.sid AND c.id=t.id
JOIN pos AS d
ON d.tid=t.tid-1 AND d.sid=t.sid AND d.id=t.id
WHERE t.pos LIKE 'J%'
AND c.token='$1'
AND ( d.token IS 'no' OR d.token IS 'not' )
GROUP BY LOWER( d.token || ' ' || t.token || ' ' || c.token )
ORDER BY frequency DESC, LOWER( d.token || ' ' || t.token || ' ' || c.token ) ASC;"

# set up, debug, do the work, and done
echo "Negative descriptions of $1"
echo -e "$HEADER$QUERY" | $DB
echo

exit
