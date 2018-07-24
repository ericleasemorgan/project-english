#!/usr/local/anaconda/bin/python

# describe.cgi - given a lemma, list the lemmatized adjectives immediately preceding it

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame, distributed under a GNU Public License

# June 13, 2018 - first investigations; 


# configure
SQL      = 'SELECT collection FROM TITLES WHERE id=?'
POSITIVE = "SELECT COUNT( LOWER( c.token || ' ' || t.token ) ) AS frequency, ( LOWER( t.token || ' ' || c.token ) ) AS phrase FROM pos AS t JOIN pos AS c ON c.tid=t.tid+1 AND c.sid=t.sid AND c.id=t.id WHERE t.pos LIKE 'J%' AND c.lemma IS ? GROUP BY LOWER( t.token || ' ' || c.token ) ORDER BY frequency DESC, LOWER( t.token || ' ' || c.token ) ASC;"
NEGATIVE = "SELECT COUNT(t.token) AS frequency, ( LOWER( d.token || ' ' || t.token || ' ' || c.token ) ) AS phrase FROM pos AS t JOIN pos AS c ON c.tid=t.tid+1 AND c.sid=t.sid AND c.id=t.id JOIN pos AS d ON d.tid=t.tid-1 AND d.sid=t.sid AND d.id=t.id WHERE t.pos LIKE 'J%' AND c.token IS ? AND ( d.token IS 'no' OR d.token IS 'not' ) GROUP BY LOWER( d.token || ' ' || t.token || ' ' || c.token ) ORDER BY frequency DESC, LOWER( d.token || ' ' || t.token || ' ' || c.token ) ASC;"
FREEBO   = '../collections/freebo/';
ECCO     = '../collections/ecco/';
SABIN    = '../collections/sabin/';
ENGLISH  = '../etc/english.db'
XYZZY    = '../carrels/xyzzy/etc/carrell.db';

# require
import cgi
import sqlite3

import cgitb
cgitb.enable()
#print( 'Content-Type: text/plain\n' )

# initialize
input = cgi.FieldStorage()

# check for input; build default page
if ( "id" not in input or 'noun' not in input ) :

	print( 'Content-Type: text/html\n' )
	print ( '''<html><head><title>Project English - Describe</title><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" href="/english/etc/style.css"></head><body><div class="header"><h1>Project English - Describe</h1></div><div class="col-3 col-m-3 menu"><ul><li><a href="/english/home.html">Home</a></li><li><a href="/english/about/">About and scope</a></li><li><a href="/english/cgi-bin/search.cgi">Search</a></li></ul></div><div class="col-9 col-m-9"><p>Given a lemmatized noun, this page will return a frequency list of two-word adjective phrases, thus "describing" the input. This is useful for gauging the sentiment towards a thing.</p><form method="GET" action="/english/cgi-bin/describe.cgi">Identifier: <input type="text" name="id" value="A27006" /><br />Lemmatized noun: <input type="text" name="noun" value="man" /><br />Type: <input type='radio' name='type' value='positive' checked='checked'>positive</input> <input type='radio' name='type' value='negative'>negative</input><br /><input type="submit" value="List descriptions" /></form><div class="footer"><p style="text-align: right">Eric Lease Morgan &amp; Team Project English<br />June 13, 2018</p></div></div></body></html>''' )

# process the input
else :
	
	# get input / initialize
	id   = input[ 'id' ].value
	noun = input[ 'noun' ].value
	type = input[ 'type' ].value

	# check for special identifier
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

	# initialize the type of assertion, positive or negative
	query = POSITIVE
	if ( type == 'negative' ) : query = NEGATIVE
	
	# initialize output
	print( 'Content-Type: text/plain\n' )
	print( 'frequency\tdescription' )

	# query the sub-database
	connection = sqlite3.connect( database )
	cursor     = connection.cursor()
	for row in cursor.execute( query, ( noun, ) ) :
		
		# parse and output
		frequency   = str( row[ 0 ] )
		description = str( row[ 1 ] )
		print( "\t".join( ( frequency, description ) ) )

# done
quit()


