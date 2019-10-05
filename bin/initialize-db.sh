#!/usr/bin/env bash

# initialize-db.sh - given a schema and set of identifiers, create an sqlite database

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame, distributed under a GNU Public License

# April 13, 2018 - first intelligent cut


# configure
HOME='/afs/crc.nd.edu/user/e/emorgan/local/html/english'
DB='./etc/english.db'
SCHEMA='./etc/schema.sql'
IDS='./etc/ids.txt'
SQL='./etc/initialization.sql'

# make sane
cd $HOME

# initialize SQL
echo "Initializing."        >&2
echo "BEGIN TRANSACTION;"   >  $SQL
#cat $SCHEMA                 >> $SQL

# process each identifier
echo "Reading identifiers." >&2
while read ID; do

	echo "INSERT INTO titles ( id ) VALUES ( '$ID' );" >> $SQL
	
done < $IDS

# finalize SQL
echo "COMMIT TRANSACTION;"     >> $SQL

# do the work
echo "Commiting."           >&2
#rm $DB
cat $SQL | sqlite3 $DB

# done
echo "Done."                >&2
exit
