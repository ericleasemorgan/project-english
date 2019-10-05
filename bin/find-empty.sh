#!/usr/bin/env bash

find collections/ecco -name "*.xml" | while read FILE; do 

	DIRECTORY=$( dirname $FILE )
	ENTITY=${FILE%.xml}.ent
	TXT=${FILE%.xml}.txt
	
	echo $DIRECTORY >&2
	echo $ENTITY    >&2
	echo $TXT       >&2
	echo            >&2
	
	if [[ ! -f $ENTITY ]]; then echo $TXT; fi
	
	
done