#!/usr/bin/perl

# id2tsv.cgi - given one more more identifiers, generate a TSV file of metatdata

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# March 9, 2017 - first cut; I'm doing great!
# April 9, 2018 - migrating to Project English


# configure
use constant QUERY  => qq(SELECT * FROM titles WHERE ##CLAUSE## ORDER BY id;);
use constant HTTP   => 'http://cds.crc.nd.edu';
#use constant HEADER => ( 'id', 'collection', 'title', 'url' );
use constant HEADER => ( 'century', 'city', 'collection', 'date', 'extent', 'id', 'imprint', 'language', 'pages', 'place', 'publisher', 'title', 'words', 'year', 'url' );

# require
use strict;
use CGI;
require '/afs/crc.nd.edu/user/e/emorgan/local/english/lib/english.pl';

# initialize
my $cgi = CGI->new;
my $ids = $cgi->param( 'ids' );
#binmode( STDOUT, ':utf8' );

# no input; display home page
if ( ! $ids ) {

	print $cgi->header;
	print &form;
	
}

# process input
else {

	# get input and sanitize it
	my @ids =  ();
	$ids    =~ s/[[:punct:]]/ /g;
	$ids    =~ s/ +/ /g;
	@ids    =  split( ' ', $ids );

	# VALIDATE INPUT HERE; we don't need to leave an opportunity for sql injection!

	# debug
	#print STDERR join( '; ', @ids ), "\n\n";

	# create the sql where clause and then build the whole sql query
	my @queries =  ();
	for my $id ( @ids ) { push( @queries, "id='$id'" ) }
	my $sql     =  QUERY;
	$sql        =~ s/##CLAUSE##/join( ' OR ', @queries )/e;

	# debug
	#print STDERR "$sql\n\n";

	# execute the query
	my $dbh    = &connect2db;
	my $handle = $dbh->prepare( $sql );
	$handle->execute() or die $DBI::errstr;

	# process each title in the found set
	my @records = ();
	while( my $titles = $handle->fetchrow_hashref ) {
	
		# parse the title data
		my $century    = $$titles{ 'century' };
		my $city       = $$titles{ 'city' };
		my $collection = $$titles{ 'collection' };
		my $date       = $$titles{ 'date' };
		my $extent     = $$titles{ 'extent' };
		my $id         = $$titles{ 'id' };
		my $imprint    = $$titles{ 'imprint' };
		my $language   = $$titles{ 'language' };
		my $pages      = $$titles{ 'pages' };
		my $place      = $$titles{ 'place' };
		my $publisher  = $$titles{ 'publisher' };
		my $title      = $$titles{ 'title' };
		my $words      = $$titles{ 'words' };
		my $year       = $$titles{ 'year' };
		
		# build the url
		my $url = HTTP . &id2root( $collection, $id );

		# debug; dump
		#print STDERR "  identifier: $id\n";
		#print STDERR "  collection: $collection\n";
		#print STDERR "       title: $title\n";
		#print STDERR "         url: $url\n";
		#print STDERR "\n";

		# create a record and then update the "database"
		my @record = ( $century, $city, $collection, $date, $extent, $id, $imprint, $language, $pages, $place, $publisher, $title, $words, $year, $url );
		push( @records, join( "\t", @record ) );
	
	}

	# dump the database and done
	print $cgi->header( -type => 'text/plain', -charset => 'utf-8');
	print join( "\t", HEADER ),   "\n";
	print join( "\n", @records ), "\n";
	
}


# done
exit;


sub form {

	return <<EOF
<html>
<head>
<title>Project English</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="/etc/style.css">
</head>
<body>
<div class="header">
	<h1>Project English - Get metadata</h1>
</div>

<div class="col-3 col-m-3 menu">
  <ul>
    <li><a href="/home.html">Home</a></li>
    <li><a href="/about/">About and scope</a></li>
	<li><a href="/cgi-bin/search.cgi">Search</a></li>
 </ul>
</div>

<div class="col-9 col-m-9">

<p>Given a set of one or more identifiers, this program will return metadata describing each item. Use the metadata for things such as: downloading full text, sorting search results, performing statistical analysis, etc. The content of this page will change automatically as searches are done against the collection.</p>
<form method='POST' action='/cgi-bin/ids2tsv.cgi'>
<input type='text' name='ids' size='50' value='1302901107 1323300900 1323600600 1346000200 1375900300 A07517 A08185 A66057 A67873 A67917 SABCPA8064301 SABCPA8094100 SABCPA8098400 SABCPA8193404 SABCPA8258500'/>
<input type='submit' value='Get metadata' />
</form>

<div class="footer">

<p style='text-align: right'>
Eric Lease Morgan &amp; Team Project English<br />
April 9, 2018
</p>

</div>

</div>


</body>
</html>
EOF
	
}


