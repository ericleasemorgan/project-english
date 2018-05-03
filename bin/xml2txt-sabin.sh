#!/bin/bash

# xml2txt.sh - transform ECCO XML to plain text
# sample usage: find SAB/CPY/709 -name '*.xml' | parallel -j12 ./bin/xml2txt.sh {}
# real	0m23.003s
# user	0m55.756s
# sys	0m32.088s

# sample usage: find SAB/CPY/709 -name '*.xml' -exec ./bin/xml2txt.sh {} \;
# real	1m12.898s
# user	0m52.945s
# sys	0m18.043s

# sample usage: find SAB/CPY/709 -name '*.xml' -exec qsub -N XML2TXT -o ./log/xml2txt  ./bin/xml2txt-sabin.sh {} \;

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under the GNU Public License

# December 22, 2017 - first cut


# configure
ROOT='/afs/crc.nd.edu/user/e/emorgan/local/english/collections/sabin'
XSLTPROC='/usr/bin/xsltproc'
STYLESHEET='./etc/xml2txt-sabin.xsl'
FILE=$1

# initialize
#cd $ROOT
ORIGINAL=$( dirname "${FILE}" )
LEAF=$( basename "$FILE" .xml )
OUTPUT="$ORIGINAL/$LEAF.txt"

# echo and do the work
echo "$FILE $OUTPUT" >&2

# do the work
$XSLTPROC --novalid $STYLESHEET $FILE 1> $OUTPUT
