#!/usr/bin/perl

# ids2zip.cgi - given one more more identifiers, create a zip file of content for downloading

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# April 19, 2017 - first investigations; need to fill out README, etc.


# configure
use constant QUERY    => qq( SELECT * FROM titles WHERE ##CLAUSE##; );
use constant ROOT     => '..';
use constant ZIPFILE  => '../tmp/search-results.zip';
use constant README   => '../etc/search-results/README';
use constant LICENSE  => '../etc/search-results/LICENSE';
use constant MANIFEST => '../etc/search-results/MANIFEST';
use constant MODEL    => '../etc/search-results/bin/model.py';
use constant CLUSTER  => '../etc/search-results/bin/cluster.py';
use constant NGRAMS   => '../etc/search-results/bin/ngrams.py';

# require
use Archive::Zip qw( :ERROR_CODES :CONSTANTS );
use CGI;
use strict;
use CGI::Carp qw(fatalsToBrowser);
require '/afs/crc.nd.edu/user/e/emorgan/local/english/lib/english.pl';

# initialize
my $cgi = CGI->new;
my $ids = $cgi->param( 'ids' );

# no input; display home page
if ( ! $ids ) {

	print $cgi->header;
	my $html = &form;
	print $html;
	
}

# process input
else {

	# initialize
	my @ids     = ();
	my @queries = ();
	my %records = ();
	
	# get input and sanitize it
	$ids =~ s/[[:punct:]]/ /g;
	$ids =~ s/ +/ /g;
	@ids =  split( ' ', $ids );

	# VALIDATE INPUT HERE; we don't need to leave an opportunity for sql injection!
	
	# initialize zipping
	my $zip = Archive::Zip->new;
	
	# add root files
	$zip->addString( &slurp( README ), "README" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
	$zip->addString( &slurp( LICENSE ), "LICENSE" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
	$zip->addString( &slurp( MANIFEST ), "MANIFEST" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
	
	# create bin directory and add scripts
	$zip->addDirectory( 'bin/' );
	$zip->addString( &slurp( MODEL ), "bin/model.py" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
	$zip->addString( &slurp( CLUSTER ), "bin/cluster.py" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
	$zip->addString( &slurp( NGRAMS ), "bin/ngrams.py" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
	
	# create directory for content
	$zip->addDirectory( 'texts/' );

	# create the sql where clause and then build the whole sql query
	for my $id ( @ids ) { push( @queries, "id='$id'" ) }
	my $sql =  QUERY;
	$sql    =~ s/##CLAUSE##/join( ' OR ', @queries )/e;

	# execute the query
	my $dbh    = &connect2db;
	my $handle = $dbh->prepare( $sql );
	$handle->execute() or die $DBI::errstr;

	# process each title in the found set
	while( my $titles = $handle->fetchrow_hashref ) {
	
		# parse
		my $collection = $$titles{ 'collection' };
		my $id         = $$titles{ 'id' };
		
		# generate file names
		my $txt = ROOT . &id2root( $collection, $id ) . "/$id.txt";
				
		# update and signal compression
		$zip->addString( &slurp( $txt ), "texts/$id.txt" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
	
	}
	
	# save
	unless ( $zip->writeToFileNamed( ZIPFILE ) == AZ_OK ) { die "Can create " . ZIPFILE . " ($!). Error" }
	
	# done
	print $cgi->header;
	my $html = &results;
	print $html;

}

# done
exit;


sub results {

	return <<EOF
<html>
<head>
<title>Project English - Download search results</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="/etc/style.css">
</head>
<body>
<div class="header">
	<h1>Project English - Download search results</h1>
</div>

<div class="col-3 col-m-3 menu">
  <ul>
    <li><a href="/home.html">Home</a></li>
    <li><a href="/about/">About and scope</a></li>
	<li><a href="/cgi-bin/search.cgi">Search</a></li>
 </ul>
</div>

<div class="col-9 col-m-9">

<p>Done. You can now <a href='/tmp/search-results.zip'>download a zip file of your search results</a>. Thank you for using Project English.</p>

	<div class="footer">
		<p style='text-align: right'>
		Eric Lease Morgan &amp; Team Project English<br />
		April 6, 2018
		</p>
	</div>

</div>


</body>
</html>
EOF
	
}


sub form {

	return <<EOF
<html>
<head>
<title>Project English - Download search results</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="/etc/style.css">
</head>
<body>
<div class="header">
	<h1>Project English - Download search results</h1>
</div>

<div class="col-3 col-m-3 menu">
  <ul>
    <li><a href="/home.html">Home</a></li>
    <li><a href="/about/">About and scope</a></li>
	<li><a href="/cgi-bin/search.cgi">Search</a></li>
 </ul>
</div>

<div class="col-9 col-m-9">

<p>Given a set of one more more Project English identifiers, this page will create an downloadable archive of the reader's search results. This will enable the reader to "read" the results in any number of ways.</p>
<p>Please be patient.</p>

<form method='POST' action='/cgi-bin/ids2zip.cgi'>
<input type='text' name='ids' size='50' value='1302901107 1323300900 1323600600 1346000200 1375900300 A07517 A08185 A66057 A67873 A67917 SABCPA8064301 SABCPA8094100 SABCPA8098400 SABCPA8193404 SABCPA8258500'/>
<input type='submit' value='Download search results' />
</form>

	<div class="footer">
		<p style='text-align: right'>
		Eric Lease Morgan &amp; Team Project English<br />
		April 6, 2018
		</p>
	</div>

</div>


</body>
</html>
EOF
	
}


