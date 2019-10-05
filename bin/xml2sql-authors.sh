#!/usr/bin/env bash

# xml2sql-authors.sh - given a filename, output an SQL statement

# sample usage: find ./collections/ecco/16 -name '*.xml' | parallel -j 8 ./bin/xml2sql-author.sh ecco {} &> ./log/xml2sql-author.log &
# sample usage: time find collections/freebo/ -name '*.xml' | parallel -j 4 ./bin/xml2sql.sh freebo {} &> ./log/xml2sql-freebo.log &
# sample usage: time find collections/freebo/ -name '*.xml' -exec qsub -N XML2SQL -o ./log/xml2sql ./bin/xml2sql.sh freebo {} &> ./log/xml2sql.log \;
# sample usage: time find collections/ecco -name '*.xml' -name '*.xml' | parallel -j 8 ./bin/xml2sql.sh ecco {} &> ./log/xml2sql-ecco.log &
# sample usage: time find collections/ecco/15/03 -name '*.xml' -exec qsub -N XML2SQL -o ./log/xml2sql ./bin/xml2sql.sh ecco {} &> ./log/xml2sql.log \;
# sample usage: time find collections/sabin -name '*.xml' -exec qsub -N XML2SQL -o ./log/xml2sql ./bin/xml2sql.sh sabin {} &> ./log/xml2sql-sabin.log \;
# sample usage: time find collections/sabin -name '*.xml' | parallel -j 4 ./bin/xml2sql.sh sabin {} &> ./log/xml2sql-sabin.log &
# sample usage: time find collections/freebo/A00 -name '*.xml' -exec ./bin/xml2sql.sh freebo {} \;

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under the GNU Public License

# April  27, 2018 - first cut, and based on other work
# October 4, 2019 - added ability determine file to process based on simple file name, not full path


# configure
HOME='/afs/crc.nd.edu/user/e/emorgan/local/html/english'
PERL5LIB='/afs/crc.nd.edu/user/e/emorgan/lib'
XML2SQLAUTHOR='./bin/xml2sql-authors.pl'
LOG='./log/xml2sql-author'
SQL='./tmp/sql-authors'
ECCO='/afs/crc.nd.edu/user/e/emorgan/local/html/english/collections/ecco'

# sanity check
if [[ -z $1 || -z $2 ]]; then
	echo "Usage: $0 <freebo|ecco|sabin> <file>" >&2
	exit
fi

# get input
COLLECTION=$1
FILE=$2

# branch according to collection
if [[ $COLLECTION == 'ecco' ]]; then

	# ecco
	BASE=$(basename $FILE .xml)
	CODE=$(echo $BASE | cut -c1-2)
	SUBCODE=$(echo $BASE | cut -c3-4)
	FILE="$ECCO/$CODE/$SUBCODE/$BASE/$BASE.xml"		
	
else
	echo "That collection is not implemented, yet. Call Eric." >&2
	exit
fi

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
	$XML2SQLAUTHOR $COLLECTION $FILE 2> $LOG 1> $OUTPUT
fi




