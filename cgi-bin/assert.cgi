#!/usr/local/anaconda/bin/python

# assert.cgi - give a lemmatized noun and a lemmatized verb, output positive and negative statements 

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame, distributed under a GNU Public License

# June 13, 2018 - first investigations; 


# configure
SQL      = 'SELECT collection FROM TITLES WHERE id=?'
POSITIVE = "SELECT COUNT( LOWER( t.token || ' ' || c.token || ' ' || d.token ) ) AS frequency , ( LOWER( t.token || ' ' || c.token || ' ' || d.token ) ) AS sentence FROM pos AS t JOIN pos AS c ON c.tid=t.tid+1 AND c.sid=t.sid AND c.id=t.id JOIN pos AS d ON d.tid=t.tid+2 AND d.sid=t.sid AND d.id=t.id WHERE t.lemma IS ? AND c.lemma IS ? AND ( d.pos LIKE 'N%' OR d.pos LIKE 'J%' ) GROUP BY ( LOWER( t.token || ' ' || c.token || ' ' || d.token ) ) ORDER BY frequency DESC, ( LOWER( t.token || ' ' || c.token || ' ' || d.token ) ) ASC;"
NEGATIVE = "SELECT COUNT( LOWER( t.token || ' ' || c.token || ' ' || d.token || ' ' || e.token ) ) AS frequency, ( LOWER( t.token || ' ' || c.token || ' ' || d.token || ' ' || e.token ) ) AS sentence FROM pos AS t JOIN pos AS c ON c.tid=t.tid+1 AND c.sid=t.sid AND c.id=t.id JOIN pos AS d ON d.tid=t.tid+2 AND d.sid=t.sid AND d.id=t.id JOIN pos AS e ON e.tid=t.tid+3 AND e.sid=t.sid AND e.id=t.id WHERE t.lemma IS ? AND c.lemma IS ? AND ( d.token IS 'no' OR d.token IS 'not' ) AND ( e.pos LIKE 'N%' OR e.pos LIKE 'J%' ) GROUP BY LOWER( t.token || ' ' || c.token || ' ' || d.token || ' ' || e.token ) ORDER BY frequency DESC, ( LOWER( t.token || ' ' || c.token || ' ' || d.token || ' ' || e.token ) ) ASC;"
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
if ( "id" not in input or 'noun' not in input or 'verb' not in input ) :

	print( 'Content-Type: text/html\n' )
	print ( '''<html><head><title>Project English - List assertions</title><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" href="/english/etc/style.css"></head><body><div class="header"><h1>Project English - List assertions</h1></div><div class="col-3 col-m-3 menu"><ul><li><a href="/english/home.html">Home</a></li><li><a href="/english/about/">About and scope</a></li><li><a href="/english/cgi-bin/search.cgi">Search</a></li></ul></div><div class="col-9 col-m-9"><p>Given a lemmatized noun and a lemmatized verb, this page will output a list positive or negative assertions in the form of noun-verb-(noun or adjective). This is useful for extracting the definitions of things, listing what things have, or listing what things do. For example, try these combinations: <a href="http://cds.crc.nd.edu/english/cgi-bin/assert.cgi?id=A27006&amp;noun=man&amp;verb=be&amp;type=positive">man be</a>, <a href="http://cds.crc.nd.edu/english/cgi-bin/assert.cgi?id=A27006&amp;noun=truth&amp;verb=be&amp;type=positive">truth be</a>, <a href="http://cds.crc.nd.edu/english/cgi-bin/assert.cgi?id=A27006&amp;noun=man&amp;verb=have&amp;type=positive">man have</a>, <a href="http://cds.crc.nd.edu/english/cgi-bin/assert.cgi?id=A27006&amp;noun=-PRON-&amp;verb=do&amp;type=positive">-PRON- do</a>. Use the summarize tool to list the frequently used lemmatized nouns, verbs, etc.</p><form method="GET" action="/english/cgi-bin/assert.cgi">Identifier: <input type="text" name="id" value="A27006" /><br />Lemmatized noun: <input type="text" name="noun" value="man" /><br />Lemmatized verb: <input type="text" name="verb" value="be" /><br />Type: <input type='radio' name='type' value='positive' checked='checked'>positive</input> <input type='radio' name='type' value='negative'>negative</input><br /><input type="submit" value="List assertions" /></form><div class="footer"><p style="text-align: right">Eric Lease Morgan &amp; Team Project English<br />June 13, 2018</p></div></div></body></html>''' )

# process the input
else :
	
	# get input / initialize
	id   = input[ 'id' ].value
	noun = input[ 'noun' ].value
	verb = input[ 'verb' ].value
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
	print( 'frequency\tassertion' )

	# query the sub-database
	connection = sqlite3.connect( database )
	cursor     = connection.cursor()
	for row in cursor.execute( query, ( noun, verb ) ) :
		
		# parse and output
		frequency = str( row[ 0 ] )
		assertion = str( row[ 1 ] )
		print( "\t".join( ( frequency, assertion ) ) )

# done
quit()


