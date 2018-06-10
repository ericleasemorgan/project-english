#!/usr/bin/env bash

# summarize.sh - report on frequencies, etc. from a Project English "study carrell"

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# June 9, 2018 - first cut; on a plane back from Prague


# configure
DB="sqlite3 ./etc/carrell.db"
HEADER=".mode tabs\n"

# sanity check
if [[ -z $1 || -z $2 ]]; then
	echo "Usage: $0 <token|lemma> <number>"
	exit
fi

# configure input
TYPE=$1
LIMIT="LIMIT $2"

# authors
N=$( echo 'SELECT COUNT( DISTINCT( author ) ) FROM authors;' | $DB )
echo "Number of authors: $N"
echo

# titles
N=$( echo 'SELECT COUNT( title ) FROM titles;' | $DB )
echo "Number of works: $N"
echo

# pages
N=$( echo 'SELECT SUM( pages ) FROM titles;' | $DB )
echo "Number of pages: $N"
echo

# words
N=$( echo 'SELECT COUNT( token ) FROM pos;' | $DB )
echo "Number of words: $N"
echo

# years
QUERY="SELECT COUNT( year ) AS frequency, year AS year FROM titles GROUP BY year ORDER BY year DESC;"
echo "Years"
echo "====="
echo -e "$HEADER$QUERY" | $DB
echo

# cities
QUERY="SELECT COUNT( city ) AS frequency, city AS city FROM titles GROUP BY city ORDER BY frequency DESC;"
echo "Publication cities"
echo "=================="
echo -e "$HEADER$QUERY" | $DB
echo

# parts-of-speech
QUERY="SELECT COUNT( pos ) AS frequency, pos AS pos FROM pos GROUP BY pos ORDER BY frequency DESC;"
echo "Parts-of-speech"
echo "==============="
echo -e "$HEADER$QUERY" | $DB
echo

# nouns
QUERY="SELECT COUNT( $TYPE ) AS frequency, $TYPE AS noun FROM pos WHERE pos LIKE 'N%' GROUP BY $TYPE ORDER BY frequency DESC $LIMIT;"
echo "Nouns ($TYPE-ized)"
echo "=================="
echo -e "$HEADER$QUERY" | $DB
echo

# pronouns
QUERY="SELECT COUNT( $TYPE ) AS frequency, $TYPE AS pronoun FROM pos WHERE pos LIKE 'PR%' GROUP BY $TYPE ORDER BY frequency DESC $LIMIT;"
echo "Pronouns ($TYPE-ized)"
echo "====================="
echo -e "$HEADER$QUERY" | $DB
echo

# verbs
QUERY="SELECT COUNT( $TYPE ) AS frequency, $TYPE AS verb FROM pos WHERE pos LIKE 'V%' GROUP BY $TYPE ORDER BY frequency DESC $LIMIT;"
echo "Verbs ($TYPE-ized)"
echo "=================="
echo -e "$HEADER$QUERY" | $DB
echo

# adjectives
QUERY="SELECT COUNT( $TYPE ) AS frequency, $TYPE AS adjective FROM pos WHERE pos LIKE 'J%' GROUP BY $TYPE ORDER BY frequency DESC $LIMIT;"
echo "Adjectives ($TYPE-ized)"
echo "======================="
echo -e "$HEADER$QUERY" | $DB
echo

# adverbs
QUERY="SELECT COUNT( $TYPE ) AS frequency, $TYPE AS adverb FROM pos WHERE pos LIKE 'RB%' GROUP BY $TYPE ORDER BY frequency DESC $LIMIT;"
echo "Adverbs ($TYPE-ized)"
echo "===================="
echo -e "$HEADER$QUERY" | $DB
echo

# entities
QUERY="SELECT COUNT( type ) AS frequency, type AS type FROM entities GROUP BY type ORDER BY frequency DESC;"
echo "Types of named entities"
echo "======================="
echo -e "$HEADER$QUERY" | $DB
echo

# people
QUERY="SELECT COUNT( entity ) AS frequency, entity AS person FROM entities WHERE type='PERSON' GROUP BY entity ORDER BY frequency DESC $LIMIT;"
echo "People"
echo "======"
echo -e "$HEADER$QUERY" | $DB
echo

# places
QUERY="SELECT COUNT( entity ) AS frequency, entity AS place FROM entities WHERE type='GPE' or type='LOC' GROUP BY entity ORDER BY frequency DESC $LIMIT;"
echo "Places"
echo "======"
echo -e "$HEADER$QUERY" | $DB
echo

# religions
QUERY="SELECT COUNT( entity ) AS frequency, entity AS norp FROM entities WHERE type='NORP' GROUP BY entity ORDER BY frequency DESC $LIMIT;"
echo "Religions"
echo "========="
echo -e "$HEADER$QUERY" | $DB
echo

# works of art
QUERY="SELECT COUNT( entity ) AS frequency, entity AS art FROM entities WHERE type='WORK_OF_ART' GROUP BY entity ORDER BY frequency DESC $LIMIT;"
echo "Works of art"
echo "============"
echo -e "$HEADER$QUERY" | $DB
echo

# languages
QUERY="SELECT COUNT( entity ) AS frequency, entity AS language FROM entities WHERE type='LANGUAGE' GROUP BY entity ORDER BY frequency DESC $LIMIT;"
echo "Languages"
echo "========="
echo -e "$HEADER$QUERY" | $DB
echo

# organizations
QUERY="SELECT COUNT( entity ) AS frequency, entity AS organization FROM entities WHERE type='ORG' GROUP BY entity ORDER BY frequency DESC $LIMIT;"
echo "Organizations"
echo "============="
echo -e "$HEADER$QUERY" | $DB
echo

# done
exit
