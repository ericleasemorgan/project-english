#!/usr/bin/env bash

# xml2sql-lcsh.sh - given a filename, output an SQL statements

# sample usage: find collections/sabin -name '*.xml' | parallel -j12 ./bin/xml2sql-lcsh.sh sabin {} &> ./log/xml2sql-lcsh.log &
# sample usage: find collections/sabin -name '*.xml' -exec qsub -N XML2LCSH -o ./log/xml2lcsh ./bin/xml2sql-lcsh.sh sabin {} &> ./log/xml2sql-lcsh.log \;

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under the GNU Public License

# June 26, 2018 - first cut, and based on other work


# configure
HOME='/afs/crc.nd.edu/user/e/emorgan/local/english'
PERL5LIB='/afs/crc.nd.edu/user/e/emorgan/lib'
XML2SQLLCSH='./bin/xml2sql-lcsh.pl'
LOG='./log/xml2sql-lcsh'
SQL='./tmp/sql-lcsh'

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
	$XML2SQLLCSH $COLLECTION $FILE 2> $LOG 1> $OUTPUT
fi




