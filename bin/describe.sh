# describe.sh - given a lemma, list the lemmatized adjectives immediately preceding it

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame and distributed under a GNU Public License

# January 3, 2018 - first cut; "Thanks go to Sean Summers for the JOIN operation!"


# configure
HOME='/afs/crc.nd.edu/user/e/emorgan/local/ecco'
DB='./etc/ecco.db'
CONFIGURE=".mode tabs\n.headers on\n"
QUERY="SELECT COUNT(t.lemma) AS n, t.lemma AS adjective
FROM words AS t
JOIN words AS c
ON c.wordid=t.wordid+1 AND c.sentenceid=t.sentenceid AND c.id=t.id
WHERE t.pos='JJ'
AND c.lemma='$1'
GROUP BY t.lemma
ORDER BY n DESC, t.lemma ASC;"

# set up, debug, do the work, and done
cd $HOME
echo -e "\n$QUERY\n" >&2
echo -e "$CONFIGURE$QUERY" | sqlite3 $DB
exit
