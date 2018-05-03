#!/usr/bin/env bash

# make-filesystem.sh - read files in a directory and move to file system
# sample usage: find xml -name *.xml | parallel ./bin/make-filesystem.sh {} \;

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame, and distributed under a GNU Public License

# July 17, 2017 - first cut and still error-prone
# April 3, 2018 - tweaked to work with parallel processing


# configure
ROOT='/afs/crc.nd.edu/user/e/emorgan/local/english/collections/freebo'
FILE=$1

# remove weird suffixes from all files
#for FILE in *.xml; do mv "$FILE" "${FILE/-[0-9.]*.xml/.xml}"; done

# re-initialize
BASE=$(basename $FILE .xml)
CODE=$(echo $BASE | cut -c1-3)
DIRECTORY="$ROOT/$CODE"

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
	

