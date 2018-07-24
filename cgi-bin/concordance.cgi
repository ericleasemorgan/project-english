#!/usr/local/anaconda/bin/python

# concordance.cgi - keyword-in-context index

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame, distributed under a GNU Public License

# April 23, 2018 - first investigations; 


DATABASE = '../etc/english.db'
SQL      = 'SELECT collection FROM TITLES WHERE id=?'
FREEBO   = '../collections/freebo/';
ECCO     = '../collections/ecco/';
SABIN    = '../collections/sabin/';
WIDTH    = 80
XYZZY    = '../carrels/xyzzy/etc/carrell.txt';

# require
from nltk        import *
from nltk.corpus import stopwords
import cgi
import sqlite3

import cgitb
cgitb.enable()
#print( 'Content-Type: text/html\n' )

# initialize
input = cgi.FieldStorage()

# check for input; build default page
if "id" not in input or "word" not in input :

	print( 'Content-Type: text/html\n' )
	print ( '''<html><head><title>Project English - Simple concordance</title><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" href="/english/etc/style.css"></head><body><div class="header"><h1>Project English - Simple concordance</h1></div><div class="col-3 col-m-3 menu"><ul><li><a href="/english/home.html">Home</a></li><li><a href="/english/about/">About and scope</a></li><li><a href="/english/cgi-bin/search.cgi">Search</a></li></ul></div><div class="col-9 col-m-9"><p>Given a Project English identifier and an word, this form returns a list of lines from the given text containing the word -- a keyword in context search result.</p><form method="GET" action="/english/cgi-bin/concordance.cgi">Identifier: <input type="text" name="id" value="1302901107" /><br />Word: <input type="text" name="word" value="love"/><br /><input type="submit" value="List lines" /></form><div class="footer"><p style="text-align: right">Eric Lease Morgan &amp; Team Project English<br />April 9, 2018</p></div></div></body></html>''' )

# process the input
else :
	
	# get input / initialize
	id         = input[ 'id' ].value
	word       = input[ 'word' ].value
	
	# check for special identifier
	if ( id == 'xyzzy' ) : file = XYZZY
	else :
	
		# open master database
		connection = sqlite3.connect( DATABASE )
		cursor     = connection.cursor()

		# identify the collection of the given id
		cursor.execute( SQL, ( id, ) )
		collection = cursor.fetchone()[0]

		if collection == 'freebo' : file = FREEBO + id[0:3] + '/'                  + id + '/' + id + '.txt'
		if collection == 'sabin'  : file = SABIN  + id[3:6] + '/' + id[6:9]  + '/' + id + '/' + id + '.txt'
		if collection == 'ecco'   : file = ECCO   + id[0:2] + '/' + id[2:4]  + '/' + id + '/' + id + '.txt'

	# open and read the desired file
	handle  = open( file, 'r', encoding='utf-8' )
	index   = ConcordanceIndex( word_tokenize( handle.read() ), key = lambda s:s.lower() )
	offsets = index.offsets( word )

	# initialize output
	print( 'Content-Type: text/plain; charset=utf-8\n' )

	# process each found item
	if offsets :

		half    = ( WIDTH - len( word ) - 2) // 2
		lines   = []
		
		for i in offsets :
	
			token = index._tokens[ i ]
			left  = index._tokens[ i - WIDTH : i ]
			right = index._tokens[ i + 1 : i + WIDTH ]
			lines.append( ' '.join([' '.join( left )[ -half : ], token, ' '.join( right )[ : half ] ] ) )

		for i, line in enumerate( lines ) : print( "% 4d) %s" % ( i + 1, line ) )
	
	else : print( "%s not found." % ( word ) )
		
# done
quit()


