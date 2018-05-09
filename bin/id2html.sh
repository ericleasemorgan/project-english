#!/usr/bin/env bash

# id2html.sh - given a file name, run id2html.pl

# usage: find collections/ecco/17/02 -name *.xml | parallel ./bin/db2solr.sh {}
# usage: T=$( echo "select count(id) from titles;" | sqlite3 ./etc/english.db ); echo "select id from titles;" | sqlite3 ./etc/english.db > ./tmp/ids.txt; C=0; while read ID; do let "C++"; echo "         item: $C of $T"; ./bin/db2solr.sh $ID; done < ./tmp/ids.txt

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame and distributed under a GNU Public License

# April 23, 2018 - first cut

# configure
HOME='/afs/crc.nd.edu/user/e/emorgan/local/english'
ID2HTML='./bin/id2html.pl'

# get input
FILE=$1

# make sane
cd $HOME
ORIGINAL=$( dirname "${FILE}" )
LEAF=$( basename "$FILE" .xml )
OUTPUT="$ORIGINAL/$LEAF.html"

# echo and do the work
echo "$LEAF  $OUTPUT" >&2

#if [ -f "$OUTPUT" ]; then
#	echo "$OUTPUT exist" >&2
#else
	$ID2HTML $LEAF 1> $OUTPUT
#fi




