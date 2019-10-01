#!/usr/bin/env bash

# txt2ent.sh - given a file name, run txt2ent.py

# usage: find collections/ecco/17/02 -name *.xml | parallel ./bin/db2solr.sh {}
# usage: T=$( echo "select count(id) from titles;" | sqlite3 ./etc/english.db ); echo "select id from titles;" | sqlite3 ./etc/english.db > ./tmp/ids.txt; C=0; while read ID; do let "C++"; echo "         item: $C of $T"; ./bin/db2solr.sh $ID; done < ./tmp/ids.txt

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame and distributed under a GNU Public License

# May 23, 2018 - first cut

# configure
HOME='/afs/crc.nd.edu/user/e/emorgan/local/html/english'
ID2ENT='./bin/txt2ent.py'

# get input
FILE=$1

# make sane
cd $HOME
ORIGINAL=$( dirname "${FILE}" )
LEAF=$( basename "$FILE" .txt )
OUTPUT="$ORIGINAL/$LEAF.ent"

# echo and do the work
echo "$LEAF  $OUTPUT" >&2

if [ -f "$OUTPUT" ]; then
	echo "$OUTPUT exist" >&2
else
	$ID2ENT $FILE 1> $OUTPUT
fi




