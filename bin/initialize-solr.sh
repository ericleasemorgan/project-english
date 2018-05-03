#!/usr/bin/env bash

# initialize-solr.sh - stop solr, delete index, and restart solr

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame, distributed under a GNU Public License

# April 17, 2018 - first intelligent cut


# configure
HOME='/afs/crc.nd.edu/user/e/emorgan/local/english'
SOLR='/usr/local/solr'
INDEX='/usr/local/solr/server/solr/english/data'

# make sane
cd $SOLR

# do the work
./bin/solr stop
rm -rf $INDEX
./bin/solr start

# go home and done
cd $HOME
exit
