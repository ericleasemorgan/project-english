#!/usr/bin/env bash

# what-is-done-by.sh - given an noun or pronoun, list the frequency of verbs immediately following it

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame and distributed under a GNU Public License

# June 9, 2018 - experimenting


# configure
DB='sqlite3 ./etc/carrell.db'
HEADER=".mode tabs\n"

# sanity check
if [[ -z $1 || -z $2 ]]; then
	echo "Usage: $0 <noun> <number>"
	exit
fi

QUERY="SELECT COUNT(t.token) AS frequency, t.token AS verb
FROM pos AS t
JOIN pos AS c
ON c.tid+1=t.tid AND c.sid=t.sid AND c.id=t.id
WHERE t.pos LIKE 'V%'
AND ( c.token='$1' AND ( c.pos LIKE 'N%' OR c.pos LIKE 'P%' ) )
GROUP BY t.token
ORDER BY frequency DESC, t.token ASC
LIMIT $2;"

# set up, debug, do the work, and done
echo "$1..., as in 'The $1 _____ ...'"
echo -e "$HEADER$QUERY" | $DB
exit
