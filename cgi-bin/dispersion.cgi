#!/usr/local/anaconda/bin/python

# dispersion.cgi - given a list of words, visualize when where they are used in a text

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame, distributed under a GNU Public License

# May 22, 2018 - first investigations; based on nltk example


DATABASE = '../etc/english.db'
SQL      = 'SELECT collection FROM TITLES WHERE id=?'
FREEBO   = '../collections/freebo/';
ECCO     = '../collections/ecco/';
SABIN    = '../collections/sabin/';
IMAGE    = '../tmp/dispersion.jpg'
XLABEL   = 'Word offsets'
TITLE    = 'Lexical dispersion'
XYZZY    = '../carrels/xyzzy/etc/carrell.txt';

# require
import matplotlib
matplotlib.use( 'Agg' )
import matplotlib.pyplot as plt
from nltk import *
import cgi
import sqlite3
import cgitb

# initialize
cgitb.enable()
print( 'Content-Type: text/html\n' )
input = cgi.FieldStorage()

# check for input; build default page
if "id" not in input or "words" not in input :

	print ( '''<html><head><title>Project English - Dispersion plot</title><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" href="/english/etc/style.css"></head><body><div class="header"><h1>Project English - Dispersion plot</h1></div><div class="col-3 col-m-3 menu"><ul><li><a href="/english/home.html">Home</a></li><li><a href="/english/about/">About and scope</a></li><li><a href="/english/cgi-bin/search.cgi">Search</a></li></ul></div><div class="col-9 col-m-9"><p>Given a Project English identifier and a list of words, visualize where the words occur in a text.</p><form method="GET" action="/english/cgi-bin/dispersion.cgi">Identifier: <input type="text" name="id" value="1302901107" /> Words: <input type="text" name="words" value="love honor justice truth beauty"/><input type="submit" value="Plot" /></form><div class="footer"><p style="text-align: right">Eric Lease Morgan &amp; Team Project English<br />April 9, 2018</p></div></div></body></html>''' )

# process the input
else :
	
	# get input / initialize
	id         = input[ 'id' ].value
	words      = input[ 'words' ].value.split()
	
	# check for special id
	if ( id == 'xyzzy' ) : file = XYZZY
	else :
	
		# open the master database
		connection = sqlite3.connect( DATABASE )
		cursor     = connection.cursor()

		# identify the collection of the given id
		cursor.execute( SQL, ( id, ) )
		collection = cursor.fetchone()[0]

		if collection == 'freebo' : file = FREEBO + id[0:3] + '/'                  + id + '/' + id + '.txt'
		if collection == 'sabin'  : file = SABIN  + id[3:6] + '/' + id[6:9]  + '/' + id + '/' + id + '.txt'
		if collection == 'ecco'   : file = ECCO   + id[0:2] + '/' + id[2:4]  + '/' + id + '/' + id + '.txt'

	# open, read, and parse the desired file
	handle   = open( file, 'r', encoding='utf-8' )
	text     = list( Text( word_tokenize( handle.read() ) ) )
	words.reverse()

	# lower-case everthing
	words_to_comp = list( map( str.lower, words ) )
	text_to_comp  = list( map( str.lower, text ) )
	
	points = [ ( x, y ) for x in range( len( text_to_comp ) )
					    for y in range( len( words_to_comp ) )
					    if text_to_comp[ x ] == words_to_comp[ y ] ]

	if points : x, y = list( zip( *points ) )
	else      : x = y = ()

	plt.plot( x, y, "b|", scalex=.1 )
	plt.yticks( list( range( len( words ) ) ), words, color="b" )
	plt.ylim( -1, len( words ) )
	plt.title( TITLE )
	plt.xlabel( XLABEL )
	plt.savefig( IMAGE )

	print ( '''<html><head><title>Project English - Dispersion plot</title><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" href="/english/etc/style.css"></head><body><div class="header"><h1>Project English - Dispersion plot</h1></div><div class="col-3 col-m-3 menu"><ul><li><a href="/english/home.html">Home</a></li><li><a href="/english/about/">About and scope</a></li><li><a href="/english/cgi-bin/search.cgi">Search</a></li></ul></div><div class="col-9 col-m-9"><img src='http://cds.crc.nd.edu/english/tmp/dispersion.jpg'/><div class="footer"><p style="text-align: right">Eric Lease Morgan &amp; Team Project English<br />April 9, 2018</p></div></div></body></html>''' )

# done
quit()


