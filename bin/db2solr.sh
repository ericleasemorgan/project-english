#!/usr/bin/env bash

# db2solr.sh - given a file name, run db2solr.pl
# usage: find collections/ecco/17/02 -name *.xml | parallel ./bin/db2solr.sh {}
# usage: T=$( echo "select count(id) from titles;" | sqlite3 ./etc/english.db ); echo "select id from titles;" | sqlite3 ./etc/english.db > ./tmp/ids.txt; C=0; while read ID; do let "C++"; echo "         item: $C of $T"; ./bin/db2solr.sh $ID; done < ./tmp/ids.txt
# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame and distributed under a GNU Public License

# December 30, 2017 - first cut for ECCO

# configure
HOME='/afs/crc.nd.edu/user/e/emorgan/local/english'
DB2SOLR='./bin/db2solr.pl'

# get input
FILE=$1

# make sane
cd $HOME
ID=$( basename "$FILE" .xml )

# do the work
$DB2SOLR $ID
