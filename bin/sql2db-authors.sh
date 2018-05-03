#!/usr/bin/env bash

# sql2db-authors.sh - the "reduce part of map/reduce for author data

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame and distributed under a GNU Public License

# April 27, 2018 - first cut, but based on other work

# configure
HOME='/afs/crc.nd.edu/user/e/emorgan/local/english'
UPDATES='./tmp/sql-authors/*.sql'
DB='./etc/english.db'
SQL='./tmp/english-authors.sql'

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
