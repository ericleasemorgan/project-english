#!/bin/bash

# xml2txt.sh - transform ECCO XML to plain text
# sample usage: find stacks -name '*.xml' | parallel ./bin/xml2txt-ecco.sh {}
# sample usage: find stacks -name '*.xml' -exec qsub -N XML2TXT -o ./log/xml2txt ./bin/xml2txt.sh {} \;

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under the GNU Public License

# December 22, 2017 - first cut


# configure
ROOT='/afs/crc.nd.edu/user/e/emorgan/local/html/english/collections/ecco'
XSLTPROC='/usr/bin/xsltproc'
STYLESHEET='./etc/xml2txt-ecco.xsl'
FILE=$1

# initialize
#cd $ROOT
ORIGINAL=$( dirname "${FILE}" )
LEAF=$( basename "$FILE" .xml )
OUTPUT="$ORIGINAL/$LEAF.txt"

# echo and do the work
echo "$FILE  $OUTPUT" >&2

if [ -f "$OUTPUT" ]; then
	echo "$OUTPUT exists" >&2
else
	$XSLTPROC --novalid $STYLESHEET $FILE 1> $OUTPUT
fi


