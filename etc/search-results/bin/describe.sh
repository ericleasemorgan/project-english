#!/usr/bin/env bash

# describe.sh - given a lemma, list the lemmatized adjectives immediately preceding it

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame and distributed under a GNU Public License

# January 3, 2018 - first cut; "Thanks go to Sean Summers for the JOIN operation!"
# June    6, 2018 - put into Project English


# configure
DB='./etc/carrell.db'
CONFIGURE=".mode tabs\n.headers on\n"

# sanity check
if [[ -z $1 ]]; then
	echo "Usage: $0 <noun>"
	exit
fi

QUERY="SELECT COUNT(t.lemma) AS frequency, t.lemma AS adjective
FROM pos AS t
JOIN pos AS c
ON c.tid=t.tid+1 AND c.sid=t.sid AND c.id=t.id
WHERE t.pos='JJ'
AND c.lemma='$1'
GROUP BY t.lemma
ORDER BY frequency DESC, t.lemma ASC;"

# set up, debug, do the work, and done
echo -e "\n$QUERY\n" >&2
echo -e "$CONFIGURE$QUERY" | sqlite3 $DB
exit
