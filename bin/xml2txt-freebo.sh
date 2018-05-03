#!/bin/bash

# xml2txt.sh - create bag o' words from xml files

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under the GNU Public License

# November 1, 2016 - first cut
# November 2, 2016 - first real run
# January 26, 2017 - ran against few file system
# June    21, 2017 - added file exists check


# configure
ROOT='/afs/crc.nd.edu/user/e/emorgan/local/english'
XSLTPROC='/usr/bin/xsltproc'
STYLESHEET='./etc/xml2txt-freebo.xsl'
FILE=$1

# initialize
cd $ROOT
ORIGINAL=$( dirname "${FILE}" )
LEAF=$( basename "$FILE" .xml )
OUTPUT="$ORIGINAL/$LEAF.txt"

# echo and do the work
echo "$FILE  $OUTPUT" >&2

if [ -f "$OUTPUT" ]; then
	echo "$OUTPUT exist" >&2
else
	$XSLTPROC --novalid $STYLESHEET $FILE 1> $OUTPUT
fi




