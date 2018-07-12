#!/usr/bin/perl

# id2urls.cgi - given one more more identifiers, generate a list of urls pointing to plain text files

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# July 12, 2018 - first cut, but based on other work


# configure
use constant QUERY  => qq(SELECT id, collection FROM titles WHERE ##CLAUSE## ORDER BY id;);
use constant HTTP   => 'http://cds.crc.nd.edu';

# require
use strict;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
require '/afs/crc.nd.edu/user/e/emorgan/local/english/lib/english.pl';

# initialize
my $cgi = CGI->new;
my $ids = $cgi->param( 'ids' );

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
		my $collection = $$titles{ 'collection' };
		my $id         = $$titles{ 'id' };
		
		# build the url
		my $url = HTTP . &id2root( $collection, $id ) . "/$id.txt";

		# debug; dump
		#print STDERR "  identifier: $id\n";
		#print STDERR "  collection: $collection\n";
		#print STDERR "       title: $title\n";
		#print STDERR "         url: $url\n";
		#print STDERR "\n";

		# create a record and then update the "database"
		my @record = ( $url );
		push( @records, join( "\t", @record ) );
	
	}

	# dump the database and done
	print $cgi->header( -type => 'text/plain', -charset => 'utf-8');
	print join( "\n", @records ), "\n";
	
}


# done
exit;


sub form {

	return <<EOF
<html>
<head>
<title>Project English - Get URLs<</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="/etc/style.css">
</head>
<body>
<div class="header">
	<h1>Project English - Get URLs</h1>
</div>

<div class="col-3 col-m-3 menu">
  <ul>
    <li><a href="/home.html">Home</a></li>
    <li><a href="/about/">About and scope</a></li>
	<li><a href="/cgi-bin/search.cgi">Search</a></li>
 </ul>
</div>

<div class="col-9 col-m-9">

<p>Given a set of one or more identifiers, this program will return a list of URLs pointing to plain text versions of items in the collection. One can then "feed" these URLs to any number of other tools for further analysis. For example, the URLs could be fed to an Internet spider cacheing the results locally.</p>
<form method='POST' action='/cgi-bin/ids2urls.cgi'>
<input type='text' name='ids' size='50' value='1302901107 1323300900 1323600600 1346000200 1375900300 A07517 A08185 A66057 A67873 A67917 SABCPA8064301 SABCPA8094100 SABCPA8098400 SABCPA8193404 SABCPA8258500'/>
<input type='submit' value='Get URLs' />
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


