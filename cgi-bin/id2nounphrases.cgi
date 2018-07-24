#!/usr/local/anaconda/bin/python

# id2nounphrases.cgi - given an identifier, return a frequency list of noun phrases 

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame, distributed under a GNU Public License

# April 23, 2018 - first investigations; 
# June  15, 2018 - added special (study carrel) identiifer


DATABASE = '../etc/english.db'
SQL      = 'SELECT collection FROM TITLES WHERE id=?'
FREEBO   = '../collections/freebo/';
ECCO     = '../collections/ecco/';
SABIN    = '../collections/sabin/';
GRAMMER  = 'NP: {<DT|PP\$>?<JJ.*>*<NN.*>+}\n{<JJ.*>*<NN*><CC>*<NN*>+}\n{<NNP>+}\n{<NN>+}'
XYZZY    = '../carrels/xyzzy/etc/carrell.txt';

# require
from nltk import RegexpParser, sent_tokenize, pos_tag, word_tokenize, FreqDist
import cgi
import sqlite3

import cgitb
cgitb.enable()
#print( 'Content-Type: text/plain\n' )

# initialize
input = cgi.FieldStorage()

# check for input; build default page
if "id" not in input :

	print( 'Content-Type: text/html\n' )
	print ( '''<html><head><title>Project English - List noun phrases</title><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" href="/english/etc/style.css"></head><body><div class="header"><h1>Project English - List noun phrases</h1></div><div class="col-3 col-m-3 menu"><ul><li><a href="/english/home.html">Home</a></li><li><a href="/english/about/">About and scope</a></li><li><a href="/english/cgi-bin/search.cgi">Search</a></li></ul></div><div class="col-9 col-m-9"><form method="GET" action="/english/cgi-bin/id2nounphrases.cgi">Identifier: <input type="text" name="id" value="SABCPA8365000" /> <input type="submit" value="List noun phrases" /></form><div class="footer"><p style="text-align: right">Eric Lease Morgan &amp; Team Project English<br />April 9, 2018</p></div></div></body></html>''' )

# process the input
else :
	
	# get input / initialize
	id         = input[ 'id' ].value
	parser     = RegexpParser( GRAMMER )
	
	# check for special identifier
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

	# open and read the desired file
	handle = open( file, 'r', encoding='utf-8' )
	data   = handle.read()

	# get all sentences and process them
	sentences = sent_tokenize( data )
	phrases   = []
	for sentence in sentences :
	
		# tokenize and tag the sentence
		sentence = ( pos_tag( word_tokenize( sentence ) ) )

		# parse the sentence and process each noun phrase
		tree = parser.parse( sentence )
		for phrase in tree.subtrees( filter = lambda t : t.label() == 'NP' ) :
		
			# re-initialize, and build up a list of normalized phrases sans determiners
			words = []
			for leaves in phrase :
				#if leaves[ 1 ] == 'DT' : continue
				words.append( leaves[ 0 ].lower() )
			phrases.append( ' '.join( words ) )

	# initialize output
	print( 'Content-Type: text/plain\n' )
	print( 'frequency\tnoun phrase' )

	# count & tabulate the phrases, output the result, and done
	frequencies = FreqDist( phrases )
	for phrase, count in frequencies.most_common() : print( "%s\t%s" % ( count, phrase ) )

# done
quit()


