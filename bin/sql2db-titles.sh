#!/usr/bin/env bash

# sql2db.sh - the "reduce part of map/reduce for bibliographic data

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame and distributed under a GNU Public License

# December 30, 2017 - first cut for ECCO

# configure
HOME='/afs/crc.nd.edu/user/e/emorgan/local/english'
UPDATES='./tmp/sql-titles/*.sql'
DB='./etc/english.db'
SQL='./tmp/english-titles.sql'

cd $HOME

# do the work
echo "Building SQL"        >&2
echo "BEGIN TRANSACTION;"  >  $SQL
cat  $UPDATES              >> $SQL
echo "COMMIT TRANSACTION;" >> $SQL

echo "Committing."         >&2
cat $SQL | sqlite3 $DB

# done
echo "Done."               >&2
exit
