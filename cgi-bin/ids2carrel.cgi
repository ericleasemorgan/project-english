#!/usr/bin/perl

# ids2zip.cgi - given one more more identifiers, create a "study carrel"

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# May 10, 2018 - first investigations
# May 11, 2018 - added different types of versions of the file

# configure
use constant CARRELS  => '../carrels';
use constant CARREL   => 'xyzzy';
use constant TEMPLATE => '../etc/template-carrel.txt';
use constant QUERY    => qq( SELECT id, collection FROM titles WHERE ##CLAUSE##; );
use constant ROOT     => '../../..';

# require
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use File::Path qw( remove_tree );
use strict;
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
	my @ids = ();
	
	# get input and sanitize it
	$ids =~ s/[[:punct:]]/ /g;
	$ids =~ s/ +/ /g;
	@ids =  split( ' ', $ids );

	# VALIDATE INPUT HERE; we don't need to leave an opportunity for sql injection!
	
	# (re-)create the file system
	my $directory = CARRELS . '/' . CARREL;
	remove_tree( $directory );
	mkdir $directory;
	mkdir "$directory/etc";
	mkdir "$directory/htm";
	mkdir "$directory/html";
	mkdir "$directory/text";
	mkdir "$directory/xml";
	
	# save the identifiers, for future reference
	open IDS, " > $directory/etc/ids.txt" or die( "Can't open $directory/etc/ids.txt ($!). Call Eric.\n" );
	foreach my $id ( @ids ) { print IDS "$id\n"; }
	close IDS;
	
	# build a query to search for collections
	my @queries = ();
	for my $id ( @ids ) { push( @queries, "id='$id'" ) }
	my $sql =  QUERY;
	$sql    =~ s/##CLAUSE##/join( ' OR ', @queries )/e;

	# find all collections
	my $dbh    = &connect2db;
	my $handle = $dbh->prepare( $sql );
	$handle->execute() or die $DBI::errstr;

	# process each item in the found set
	while( my $item = $handle->fetchrow_hashref ) {
	
		# parse
		my $collection = $$item{ 'collection' };
		my $id         = $$item{ 'id' };
		
		# generate file names
		my $root = ROOT . &id2root( $collection, $id );
		symlink( "$root/$id.htm",  "$directory/htm/$id.htm" );
		symlink( "$root/$id.html", "$directory/html/$id.html" );
		symlink( "$root/$id.txt",  "$directory/text/$id.txt" );
		symlink( "$root/$id.xml",  "$directory/xml/$id.xml" );
	
	}

	my $options = '';
	foreach my $id ( @ids ) { $options .= "<option value='$id'>$id</option>" }
	
	my $html = &slurp( TEMPLATE );
	$html =~ s/##OPTIONS##/$options/g;
	$html =~ s/##IDS##/$ids/g;
	
	open HTML, " > $directory/home.html" or die( "Can't open $directory/home.html ($!). Call Eric.\n" );
	print HTML $html;
	close HTML;
	
	# done
	print $cgi->redirect( 'http://cds.crc.nd.edu/carrels/xyzzy/');

}

# done
exit;


sub form {

	return <<EOF
<html>
<head>
<title>Project English - DCreate study carrel</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="/etc/style.css">
</head>
<body>
<div class="header">
	<h1>Project English - Create study carrel</h1>
</div>

<div class="col-3 col-m-3 menu">
  <ul>
    <li><a href="/home.html">Home</a></li>
    <li><a href="/about/">About and scope</a></li>
	<li><a href="/cgi-bin/search.cgi">Search</a></li>
 </ul>
</div>

<div class="col-9 col-m-9">

<p>Given a set of one more more Project English identifiers, this page will create a "study carrel".</p>
<p>Please be patient.</p>

<form method='POST' action='/cgi-bin/ids2carrel.cgi'>
<input type='text' name='ids' size='50' value='1302901107 1323300900 1323600600 1346000200 1375900300 A07517 A08185 A66057 A67873 A67917 SABCPA8064301 SABCPA8094100 SABCPA8098400 SABCPA8193404 SABCPA8258500'/>
<input type='submit' value='Make carrel' />
</form>

	<div class="footer">
		<p style='text-align: right'>
		Eric Lease Morgan &amp; Team Project English<br />
		May 10, 2018
		</p>
	</div>

</div>

</body>
</html>
EOF
	
}


