#!/usr/local/anaconda/bin/python

# posnet.cgi - list the frequency of selected parts-of-speech and named-entities

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame, distributed under a GNU Public License

# June 13, 2018 - first investigations; 


# configure
SQL      = 'SELECT collection FROM TITLES WHERE id=?'
FREEBO   = '../collections/freebo/';
ECCO     = '../collections/ecco/';
SABIN    = '../collections/sabin/';
ENGLISH  = '../etc/english.db'
XYZZY    = '../carrels/xyzzy/etc/carrell.db';
QUERIES  = { 'pos'            : "SELECT COUNT( pos )    AS f, pos     FROM pos                               GROUP BY pos    ORDER BY f DESC;",
            'nouns'           : "SELECT COUNT( token )  AS f, token   FROM pos      WHERE pos LIKE 'N%'      GROUP BY token  ORDER BY f DESC;",
            'nounslemma'      : "SELECT COUNT( lemma )  AS f, lemma   FROM pos      WHERE pos LIKE 'N%'      GROUP BY lemma  ORDER BY f DESC;",
            'pronouns'        : "SELECT COUNT( token )  AS f, token   FROM pos      WHERE pos LIKE 'PR%'     GROUP BY token  ORDER BY f DESC;",
            'pronounslemma'   : "SELECT COUNT( lemma )  AS f, lemma   FROM pos      WHERE pos LIKE 'PR%'     GROUP BY lemma  ORDER BY f DESC;",
            'verbs'           : "SELECT COUNT( token )  AS f, token   FROM pos      WHERE pos LIKE 'V%'      GROUP BY token  ORDER BY f DESC;",
            'verbslemma'      : "SELECT COUNT( lemma )  AS f, lemma   FROM pos      WHERE pos LIKE 'V%'      GROUP BY lemma  ORDER BY f DESC;",
            'adjectives'      : "SELECT COUNT( token )  AS f, token   FROM pos      WHERE pos LIKE 'J%'      GROUP BY token  ORDER BY f DESC;",
            'adjectiveslemma' : "SELECT COUNT( lemma )  AS f, lemma   FROM pos      WHERE pos LIKE 'J%'      GROUP BY lemma  ORDER BY f DESC;",
            'adverbs'         : "SELECT COUNT( token )  AS f, token   FROM pos      WHERE pos LIKE 'RB%'     GROUP BY token  ORDER BY f DESC;",
            'adverbslemma'    : "SELECT COUNT( lemma )  AS f, lemma   FROM pos      WHERE pos LIKE 'RB%'     GROUP BY lemma  ORDER BY f DESC;",
            'entities'        : "SELECT COUNT( type )   AS f, type    FROM entities                          GROUP BY type   ORDER BY f DESC;",
            'people'          : "SELECT COUNT( entity ) AS f, entity  FROM entities WHERE type='PERSON'      GROUP BY entity ORDER BY f DESC;",
            'religions'       : "SELECT COUNT( entity ) AS f, entity  FROM entities WHERE type='NORP'        GROUP BY entity ORDER BY f DESC;",
            'worksofart'      : "SELECT COUNT( entity ) AS f, entity  FROM entities WHERE type='WORK_OF_ART' GROUP BY entity ORDER BY f DESC;",
            'languages'       : "SELECT COUNT( entity ) AS f, entity  FROM entities WHERE type='LANGUAGE'    GROUP BY entity ORDER BY f DESC;",
            'organizations'   : "SELECT COUNT( entity ) AS f, entity  FROM entities WHERE type='ORG'         GROUP BY entity ORDER BY f DESC;",
            'places'          : "SELECT COUNT( entity ) AS f, entity  FROM entities WHERE type='GPE' or type='LOC' GROUP BY entity ORDER BY f DESC;" }


# require
import cgi
import sqlite3

import cgitb
cgitb.enable()
#print( 'Content-Type: text/plain\n' )

# initialize
input = cgi.FieldStorage()

# check for input; build default page
if ( "id" not in input or 'type' not in input ) :

	print( 'Content-Type: text/html\n' )
	print ( '''<html><head><title>Project English - Parts-of-speech &amp; named-entities</title><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" href="/english/etc/style.css"></head><body><div class="header"><h1>Project English - Parts-of-speech &amp; named-entities</h1></div><div class="col-3 col-m-3 menu"><ul><li><a href="/english/home.html">Home</a></li><li><a href="/english/about/">About and scope</a></li><li><a href="/english/cgi-bin/search.cgi">Search</a></li></ul></div><div class="col-9 col-m-9"><p>Use this page to list the frequency of selected parts-of-speech and named entities existing in a document. This is is useful for gauging what & how things are discussed.</p><form method="GET" action="/english/cgi-bin/posent.cgi">Identifier: <input type="text" name="id" value="A27006" /><br />Selection: <select name='type'>
<option value='pos'>types of parts-of-speech</option>
<option value='nouns'>nouns</option>
<option value='nounslemma'>lemmatized nouns</option>
<option value='pronouns'>pronouns</option>
<option value='pronounslemma'>lemmatized pronouns</option>
<option value='verbs'>verbs</option>
<option value='verbslemma'>lemmatized verbs</option>
<option value='adjectives'>adjectives</option>
<option value='adjectiveslemma'>lemmatized adjectives</option>
<option value='adverbs'>adverbs</option>
<option value='adverbslemma'>lemmatized adverbs</option>
<option value='entities'>types of named-entities</option>
<option value='people'>people</option>
<option value='places'>places</option>
<option value='organizations'>organizations</option>
<option value='religions'>religions</option>
<option value='worksofart'>works of art</option>
<option value='languages'>languages</option>
</select></br>
	<input type="submit" value="List items" /></form><div class="footer"><p style="text-align: right">Eric Lease Morgan &amp; Team Project English<br />June 13, 2018</p></div></div></body></html>''' )

# process the input
else :
	
	# get input / initialize
	id   = input[ 'id' ].value
	type = input[ 'type' ].value

	# trap for special identifier
	if ( id == 'xyzzy' ) : database = XYZZY
	else :
	
		# query the master database for the collection name, and then compute the location of the sub-database
		connection = sqlite3.connect( ENGLISH )
		cursor     = connection.cursor()
		cursor.execute( SQL, ( id, ) )
		collection = cursor.fetchone()[0]
		if collection == 'freebo' : database = FREEBO + id[0:3] + '/'                  + id + '/' + id + '.db'
		if collection == 'sabin'  : database = SABIN  + id[3:6] + '/' + id[6:9]  + '/' + id + '/' + id + '.db'
		if collection == 'ecco'   : database = ECCO   + id[0:2] + '/' + id[2:4]  + '/' + id + '/' + id + '.db'
	
	# initialize output
	print( 'Content-Type: text/plain\n' )
	print( 'frequency\titem' )

	# query the sub-database
	connection = sqlite3.connect( database )
	cursor     = connection.cursor()
	for row in cursor.execute( QUERIES[ type ] ) :
		
		# parse and output
		frequency = str( row[ 0 ] )
		item      = str( row[ 1 ] )
		print( "\t".join( ( frequency, item ) ) )

# done
quit()


