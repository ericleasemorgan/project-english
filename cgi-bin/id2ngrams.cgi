#!/usr/local/anaconda/bin/python

# id2ngrams.cgi - given an identifier and an integer, return a frequency list of ngrams

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame, distributed under a GNU Public License

# April  23, 2018 - first investigations; 
# August 22, 2018 - fixed stupid ascii/utf-8 encoding error; Yeah!

# configure
DATABASE = '../etc/english.db'
SQL      = 'SELECT collection FROM TITLES WHERE id=?'
FREEBO   = '../collections/freebo/';
ECCO     = '../collections/ecco/';
SABIN    = '../collections/sabin/';
XYZZY    = '../carrels/xyzzy/etc/carrell.txt';

# require
from nltk        import word_tokenize, ngrams, FreqDist
from nltk.corpus import stopwords
import cgi
import codecs
import sqlite3
import sys
import cgitb
cgitb.enable()
#print( 'Content-Type: text/html\n' )

# initialize
input      = cgi.FieldStorage()
sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)

# check for input; build default page
if "id" not in input or "n" not in input :

	print( 'Content-Type: text/html\n' )
	print ( '''<html><head><title>Project English - List ngrams</title><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" href="/english/etc/style.css"></head><body><div class="header"><h1>Project English - List ngrams</h1></div><div class="col-3 col-m-3 menu"><ul><li><a href="/english/home.html">Home</a></li><li><a href="/english/about/">About and scope</a></li><li><a href="/english/cgi-bin/search.cgi">Search</a></li></ul></div><div class="col-9 col-m-9"><p>Given a Project English identifier and an integer, this form returns a frequency list of ngrams (i.e. one-word, two-word, three-word phrases) from the identified text. Save the result and do further analysis with the use of your favorite text editor, spreadsheet, database, or statistics application(s).</p><form method="GET" action="/english/cgi-bin/id2ngrams.cgi">Identifier: <input type="text" name="id" value="1302901107" /><br />Size of ngram: <input type="text" name="n" value="2" size='2' width='2' /><br /><input type="submit" value="List ngrams" /></form><div class="footer"><p style="text-align: right">Eric Lease Morgan &amp; Team Project English<br />April 9, 2018</p></div></div></body></html>''' )

# process the input
else :
	
	# get input / initialize
	id         = input[ 'id' ].value
	n          = int( input[ 'n' ].value )
	stopwords  = stopwords.words( 'english' )

	# trap special identifier
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
	handle = open( file, 'r', encoding='utf-8' )
	data   = handle.read()

	# tokenize the text into features, normalize, and remove (English) stopwords
	features = word_tokenize( data )
	features = [ feature for feature in features if feature.isalpha() ]
	features = [ feature.lower() for feature in features ]
	features = [ feature for feature in features if feature not in stopwords ]

	# create ngrams; count & tabulate them
	ngrams      = ngrams( features, n )
	frequencies = FreqDist( ngrams )
	
	# initialize output
	print( 'Content-Type: text/plain; charset=utf-8\n' )
	print( 'frequency\tngram' )
	
	# loop through each frequency and output
	for ngram, count in frequencies.most_common() : print( "%s\t%s" % ( count, ' '.join( ngram ) ) )

# done
quit()


