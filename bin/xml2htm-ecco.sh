#!/usr/bin/env bash

# xml2htm-ecco.sh - create rudimentary HTML from XML
# usage: find collections/ecco -name *.xml | parallel -j12 ./bin/xml2htm-ecco.sh {} 

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under the GNU Public License

# April 6, 2018


# configure
ROOT='/afs/crc.nd.edu/user/e/emorgan/local/english'
XSLTPROC='/usr/bin/xsltproc'
STYLESHEET='./etc/xml2htm-ecco.xsl'
FILE=$1

# initialize
cd $ROOT
ORIGINAL=$( dirname "${FILE}" )
LEAF=$( basename "$FILE" .xml )
OUTPUT="$ORIGINAL/$LEAF.htm"

# echo and do the work
echo "$FILE  $OUTPUT" >&2

if [ -f "$OUTPUT" ]; then
	echo "$OUTPUT exists" >&2
else
	$XSLTPROC --novalid $STYLESHEET $FILE 1> $OUTPUT
fi



