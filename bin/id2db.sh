#!/usr/bin/env bash

# id2db.sh - given a file name, run id2db.pl
# usage: find collections/ecco/17/02 -name *.xml | parallel ./bin/db2db.sh {}

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame and distributed under a GNU Public License

# June 12, 2018 - first cut

# configure
HOME='/afs/crc.nd.edu/user/e/emorgan/local/html/english'
ID2DB='./bin/id2db.pl'

# get input
FILE=$1

# make sane
cd $HOME
DIRECTORY=$( dirname "${FILE}" )

# echo and do the work
echo "$DIRECTORY" >&2
$ID2DB $DIRECTORY