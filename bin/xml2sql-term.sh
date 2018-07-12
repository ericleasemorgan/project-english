#!/usr/bin/env bash

# xml2sql-term.sh - given a filename, output an SQL statements

# sample usage: find collections/freebo -name '*.xml' | parallel -j12 ./bin/xml2sql-term.sh freebo {} &> ./log/xml2sql-term.log &
# sample usage: find collections/freebo -name '*.xml' -exec qsub -N XML2TERM -o ./log/xml2term ./bin/xml2sql-term.sh freebo {} &> ./log/xml2sql-term.log \;

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under the GNU Public License

# June 26, 2018 - first cut, and based on other work


# configure
HOME='/afs/crc.nd.edu/user/e/emorgan/local/english'
PERL5LIB='/afs/crc.nd.edu/user/e/emorgan/lib'
XML2SQLTERM='./bin/xml2sql-term.pl'
LOG='./log/xml2sql-term'
SQL='./tmp/sql-term'

# get input
COLLECTION=$1
FILE=$2

# sanity
cd $HOME
mkdir -p $LOG
mkdir -p $SQL

# initialize
LEAF=$( basename "$FILE" .xml )
OUTPUT="$SQL/$LEAF.sql"
LOG="$LOG/$LEAF.log"

if [ -f "$OUTPUT" ]; then
	echo "$OUTPUT exists" >&2
else
	echo "$FILE" >&2
	$XML2SQLTERM $COLLECTION $FILE 2> $LOG 1> $OUTPUT
fi




