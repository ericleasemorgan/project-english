#!/usr/bin/env bash

# xml2sql.sh - create bag o' words from xml files
# sample usage: find collections/ecco/16 -name '*.xml' | parallel -j 15 ./bin/xml2sql.sh ecco {} &> ./log/xml2sql.log &
# sample usage: time find collections/freebo/ -name '*.xml' | parallel -j 4 ./bin/xml2sql.sh freebo {} &> ./log/xml2sql-freebo.log &
# sample usage: time find collections/freebo/ -name '*.xml' -exec qsub -N XML2SQL -o ./log/xml2sql ./bin/xml2sql.sh freebo {} &> ./log/xml2sql.log \;
# sample usage: time find collections/ecco -name '*.xml' -name '*.xml' | parallel -j 8 ./bin/xml2sql.sh ecco {} &> ./log/xml2sql-ecco.log &
# sample usage: time find collections/ecco/15/03 -name '*.xml' -exec qsub -N XML2SQL -o ./log/xml2sql ./bin/xml2sql.sh ecco {} &> ./log/xml2sql.log \;
# sample usage: time find collections/sabin -name '*.xml' -exec qsub -N XML2SQL -o ./log/xml2sql ./bin/xml2sql.sh sabin {} &> ./log/xml2sql-sabin.log \;
# sample usage: time find collections/sabin -name '*.xml' | parallel -j 4 ./bin/xml2sql.sh sabin {} &> ./log/xml2sql-sabin.log &
# sample usage: time find collections/freebo/A00 -name '*.xml' -exec ./bin/xml2sql.sh freebo {} \;

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under the GNU Public License

# December 12, 2017 - a hack when nobody is here


# configure
HOME='/afs/crc.nd.edu/user/e/emorgan/local/html/english'
PERL5LIB='/afs/crc.nd.edu/user/e/emorgan/lib'
XML2SQL='./bin/xml2sql-titles.pl'

# get input
COLLECTION=$1
FILE=$2

# initialize
SQL="./tmp/sql-titles-$COLLECTION"
LOG="./log/xml2sql-titles-$COLLECTION"

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
	$XML2SQL $COLLECTION $FILE 2> $LOG 1> $OUTPUT
fi




