#!/usr/local/anaconda/bin/python

# compare.cgi - given a type of part-of-speech, output a list of conjunctions

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame, distributed under a GNU Public License

# June 20, 2018 - first investigations; 


# configure
SQL      = 'SELECT collection FROM TITLES WHERE id=?'
QUERY    = "SELECT COUNT( LOWER( t.token || ' ' || c.token || ' ' || d.token ) ) AS frequency , ( LOWER( t.token || ' ' || c.token || ' ' || d.token ) ) AS sentence FROM pos AS t JOIN pos AS c ON c.tid=t.tid+1 AND c.sid=t.sid AND c.id=t.id JOIN pos AS d ON d.tid=t.tid+2 AND d.sid=t.sid AND d.id=t.id WHERE ( t.pos LIKE ? AND c.POS IS 'CC' AND d.pos LIKE ? ) GROUP BY ( LOWER( t.token || ' ' || c.token || ' ' || d.token ) ) ORDER BY frequency DESC, ( LOWER( t.token || ' ' || c.token || ' ' || d.token ) ) ASC;"
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
if ( "id" not in input or 'type' not in input ) :

	print( 'Content-Type: text/html\n' )
	print ( '''<html><head><title>Project English - Compare &amp; contrast</title><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" href="/etc/style.css"></head><body><div class="header"><h1>Project English - Compare &amp; contrast</h1></div><div class="col-3 col-m-3 menu"><ul><li><a href="/home.html">Home</a></li><li><a href="/about/">About and scope</a></li><li><a href="/cgi-bin/search.cgi">Search</a></li></ul></div><div class="col-9 col-m-9"><p>Given a type of part-of-speech (noun, verb, or adjective), this page will output a frequency list of conjunctions: this and that, one or another, etc. This helps answer the question, "What is compared &amp; contrasted in this text or corpus?"</p><form method="GET" action="/cgi-bin/compare.cgi">Identifier: <input type="text" name="id" value="A27006" /><br />Type of comparison: <input type="radio" name="type" value="N" checked='checked'> noun</input>  <input type="radio" name="type" value="V"> verb</input>  <input type="radio" name="type" value="J"> adjective</input><br /><input type="submit" value="List comparisons" /></form><div class="footer"><p style="text-align: right">Eric Lease Morgan &amp; Team Project English<br />June 20, 2018</p></div></div></body></html>''' )

# process the input
else :
	
	# get input / initialize
	id   = input[ 'id' ].value
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

	# initialize the query and type of comparison
	query = QUERY
	type  = type + '%'
	
	# initialize output
	print( 'Content-Type: text/plain\n' )
	print( 'frequency\tassertion' )

	# query the sub-database
	connection = sqlite3.connect( database )
	cursor     = connection.cursor()
	for row in cursor.execute( query, ( type, type ) ) :
		
		# parse and output
		frequency  = str( row[ 0 ] )
		comparison = str( row[ 1 ] )
		print( "\t".join( ( frequency, comparison ) ) )

# done
quit()


