#!/usr/bin/env bash

# make-filesystem.sh - given a file name, create a directory and copy the file accordingly
# sample usage: find xml -name *.xml | parallel ./bin/make-filesystem.sh {} \;
 
# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame, and distributed under a GNU Public License

# December 22, 2017 - first cut


# configure
ROOT='/afs/crc.nd.edu/user/e/emorgan/local/html/english/collections/ecco'
FILE=$1

# initialize
BASE=$(basename $FILE .xml)
CODE=$(echo $BASE | cut -c1-2)
SUBCODE=$(echo $BASE | cut -c3-4)
DIRECTORY="$ROOT/$CODE/$SUBCODE"		

# check to see if the directory already exits
if [ ! -d "$DIRECTORY/$BASE" ]; then

	# create directory structure
	echo "Creating directory $DIRECTORY/$BASE" >&2
	mkdir $BASE
	cp $FILE $BASE
	chmod -R 700 $BASE
	mkdir -p $DIRECTORY
	mv -f $BASE $DIRECTORY
			
else

	# simply move the file 
	echo "Exists; copying $FILE to $DIRECTORY/$BASE" >&2
	cp $FILE "$DIRECTORY/$BASE"
	chmod 700 "$DIRECTORY/$BASE/$FILE"
	
fi
