#!/usr/bin/env bash

# filesystem2ids.sh - extract basename of files, used to get sets of database keys

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame, distributed under a GNU Public License

# April 13, 2018 - first investigations


FILE=$1
ID=$( basename $FILE .xml )
echo $ID
exit
