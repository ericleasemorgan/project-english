#!/usr/bin/perl

# ids2carrel.cgi - given one more more identifiers, create a "study carrel"

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# May 10, 2018 - first investigations
# May 11, 2018 - added different types of versions of the file


# configure
use constant CARRELLDB  => '../carrels/xyzzy/etc/carrell.db';
use constant CARRELLTXT => '../carrels/xyzzy/etc/carrell.txt';
use constant CARRELLSQL => '../etc/carrell.sql';
use constant CARRELS    => '../carrels';
use constant CARREL     => 'xyzzy';
use constant DRIVER     => 'SQLite';
use constant TEMPLATE   => '../etc/template-carrel.txt';
use constant ROOT       => '../../..';
use constant SIZE       => 55;
use constant HOME       => 'http://cds.crc.nd.edu/english/carrels/xyzzy/home.html';

# require
use CGI;
use CGI::Carp qw( fatalsToBrowser );
use File::Path qw( remove_tree );
use strict;
require '/afs/crc.nd.edu/user/e/emorgan/local/html/english/lib/english.pl';

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
	mkdir "$directory/ent";
	mkdir "$directory/pos";
	
	# save the identifiers, for future reference
	open IDS, " > $directory/etc/ids.txt" or die( "Can't open $directory/etc/ids.txt ($!). Call Eric.\n" );
	foreach my $id ( @ids ) { print IDS "$id\n"; }
	close IDS;
	
	# delete, open, and initialize a study carrel database
	unlink( ( CARRELLDB ) );
	my $database = CARRELLDB;
	my $driver   = DRIVER;
	my $carrell  = DBI->connect( "DBI:$driver:dbname=$database", '', '', { RaiseError => 1 } ) or die $DBI::errstr;
	foreach my $statement ( split ";", &slurp( CARRELLSQL ) ) { $carrell->do( $statement ) }

	# open a connect to the master database
	my $english = &connect2db;

	my $corpus = CARRELLTXT;
	
	# process each of the given ids
	foreach my $id ( @ids ) {

		# given the id, find its collection
		my $handle = $english->prepare( "SELECT collection FROM titles WHERE id IS '$id'" );
		$handle->execute() or die $DBI::errstr;
 		my $collection = $handle->fetchrow_array();
 		
		# get the root of the individual item
		my $root = ROOT . &id2root( $collection, $id );
		
		# symbolically link files locally
		symlink( "$root/$id.htm",  "$directory/htm/$id.htm" );
		symlink( "$root/$id.html", "$directory/html/$id.html" );
		symlink( "$root/$id.txt",  "$directory/text/$id.txt" );
		symlink( "$root/$id.xml",  "$directory/xml/$id.xml" );
		symlink( "$root/$id.ent",  "$directory/ent/$id.ent" );
		symlink( "$root/$id.pos",  "$directory/pos/$id.pos" );
	
		# build up the corpus
		my $item = '../' . &id2root( $collection, $id ) . "/$id.txt";
		open CORPUS, ">> $corpus" or die "Could not open $corpus ($!). Call Eric.\n";
		open ITEM,   "< $item"    or die "Could not open $item ($!). Call Eric.\n";
		print CORPUS $_ while <ITEM>;
		print CORPUS "\n=====\n";
		close ITEM;
		close CORPUS;
				
		# generate the name of the item's database, and copy its contents
		my $db  = '../' . &id2root( $collection, $id ) . "/$id.db";
		$carrell->do( qq( ATTACH "$db" AS 'item'; ) );
		$carrell->do( qq( INSERT INTO titles   SELECT * FROM item.titles   WHERE id IS '$id'; ) );
		$carrell->do( qq( INSERT INTO authors  SELECT * FROM item.authors  WHERE id IS '$id'; ) );
		$carrell->do( qq( INSERT INTO pos      SELECT * FROM item.pos      WHERE id IS '$id'; ) );
		$carrell->do( qq( INSERT INTO entities SELECT * FROM item.entities WHERE id IS '$id'; ) );
		$carrell->do( qq( DETACH DATABASE 'item'; ) );
		
	}

	# close the database connections
	$carrell->disconnect;
	$english->disconnect;
	
	my $html = &slurp( TEMPLATE );
	$html =~ s/##TOTAL##/scalar( @ids )/eg;
	$html =~ s/##IDS##/$ids/g;
	
	open HTML, " > $directory/home.html" or die( "Can't open $directory/home.html ($!). Call Eric.\n" );
	print HTML $html;
	close HTML;
	
	# done
	print $cgi->redirect( HOME );

}

# done
exit;


sub form {

	return <<EOF
<html>
<head>
<title>Project English - Create study carrel</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="/english/etc/style.css">
</head>
<body>
<div class="header">
	<h1>Project English - Create study carrel</h1>
</div>

<div class="col-3 col-m-3 menu">
  <ul>
    <li><a href="/english/home.html">Home</a></li>
    <li><a href="/english/about/">About</a></li>
    <li><a href="/english/cgi-bin/search.cgi">Search</a></li>
    <li><a href="/english/tools.html">Extra tools</a></li>
 </ul>
</div>

<div class="col-9 col-m-9">

<p>Given a set of one more more Project English identifiers, this page will create a "study carrel".</p>
<p>Please be patient.</p>

<form method='POST' action='/english/cgi-bin/ids2carrel.cgi'>
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


