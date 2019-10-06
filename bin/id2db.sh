#!/usr/bin/env bash

# id2db.sh - given a file name, run id2db.pl
# usage: find collections/ecco/17/02 -name *.xml | parallel ./bin/db2db.sh {}

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame and distributed under a GNU Public License

# June   12, 2018 - first cut
# October 6, 2019 - give it more thorough command-line input


# configure
HOME='/afs/crc.nd.edu/user/e/emorgan/local/html/english'
ID2DB='./bin/id2db.pl'
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
	DIRECTORY="$ECCO/$CODE/$SUBCODE/$BASE/"		
	
else
	echo "That collection is not implemented, yet. Call Eric." >&2
	exit
fi

# make sane
cd $HOME

# echo and do the work
echo "$DIRECTORY" >&2
$ID2DB $DIRECTORY