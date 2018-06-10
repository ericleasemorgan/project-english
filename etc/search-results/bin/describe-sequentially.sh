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
if [[ -z $1 || -z $2 ]]; then
	echo "Usage: $0 <noun> <number>"
	exit
fi

QUERY="SELECT t.sid AS s, t.token AS adjective
FROM pos AS t
JOIN pos AS c
ON c.tid=t.tid+1 AND c.sid=t.sid AND c.id=t.id
WHERE t.pos LIKE 'J%'
AND c.token='$1'
ORDER BY s DESC, t.token ASC
LIMIT $2"

# set up, debug, do the work, and done
echo "$1 is described as ____, as in 'The _____ $1...'"
echo -e "$HEADER$QUERY" | $DB
exit
