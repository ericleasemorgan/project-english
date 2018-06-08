#!/usr/bin/perl

# ids2zip.cgi - given one more more identifiers, create a zip file of content for downloading

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# April 19, 2018 - first investigations; need to fill out README, etc.
# June   6, 2018 - added some scripts as well as ent & pos files
# June   8, 2018 - added title, author, entity, and pos data to database while at ELAG 2018; jeesh!


# configure
use constant QUERY        => qq( SELECT * FROM titles WHERE ##CLAUSE##; );
use constant ROOT         => '..';
use constant ZIPFILE      => '../tmp/search-results.zip';
use constant README       => '../etc/search-results/README';
use constant LICENSE      => '../etc/search-results/LICENSE';
use constant MANIFEST     => '../etc/search-results/MANIFEST';
use constant MODEL        => '../etc/search-results/bin/model.py';
use constant CLUSTER      => '../etc/search-results/bin/cluster.py';
use constant NGRAMS       => '../etc/search-results/bin/ngrams.py';
use constant NOUNPHRASES  => '../etc/search-results/bin/noun-phrases.py';
use constant STOPWORDS    => '../etc/search-results/etc/stopwords.txt';
use constant DESCRIBE     => '../etc/search-results/bin/describe.sh';
use constant CARRELLDB    => '../tmp/carrell.db';
use constant CARRELLSQL   => '../etc/carrell.sql';
use constant DRIVER       => 'SQLite';

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
	$zip->addFile( README, "README" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
	$zip->addFile( LICENSE, "LICENSE" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
	$zip->addFile( MANIFEST, "MANIFEST" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
	
	# create bin directory and add scripts
	$zip->addDirectory( 'bin/' );
	$zip->addFile( MODEL, "bin/model.py" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
	$zip->addFile( CLUSTER, "bin/cluster.py" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
	$zip->addFile( NGRAMS, "bin/ngrams.py" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
	$zip->addFile( NOUNPHRASES, "bin/noun-phrases.py" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
	$zip->addFile( DESCRIBE, "bin/describe.sh" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
	
	# create etc directory and add... stuff
	$zip->addDirectory( 'etc/' );
	$zip->addFile( STOPWORDS, "etc/stopwords.txt" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
	
	# create directories for content
	$zip->addDirectory( 'txt/' );
	$zip->addDirectory( 'ent/' );
	$zip->addDirectory( 'pos/' );

	# create the sql WHERE clause and then build the whole sql query
	for my $id ( @ids ) { push( @queries, "id='$id'" ) }
	my $sql =  QUERY;
	$sql    =~ s/##CLAUSE##/join( ' OR ', @queries )/e;

	# execute the query
	my $dbh    = &connect2db;
	my $handle = $dbh->prepare( $sql );
	$handle->execute() or die $DBI::errstr;

	# delete, open, and initialize a study carrell database
	unlink( ( CARRELLDB ) );
	my $database = CARRELLDB;
	my $driver   = DRIVER;
	my $carrell  = DBI->connect( "DBI:$driver:dbname=$database", '', '', { RaiseError => 1 } ) or die $DBI::errstr;
	foreach my $statement ( split ";", &slurp( CARRELLSQL ) ) { $carrell->do( $statement ) }

	# process each title in the found set
	while( my $item = $handle->fetchrow_hashref ) {
	
		# parse
		my $century    = $$item{ 'century' };
		my $city       = $$item{ 'city' };
		my $collection = $$item{ 'collection' };
		my $date       = $$item{ 'date' };
		my $extent     = $$item{ 'extent' };
		my $id         = $$item{ 'id' };
		my $imprint    = $$item{ 'imprint' };
		my $language   = $$item{ 'language' };
		my $pages      = $$item{ 'pages' };
		my $place      = $$item{ 'place' };
		my $publisher  = $$item{ 'publisher' };
		my $title      = $$item{ 'title' };
		my $words      = $$item{ 'words' };
		my $year       = $$item{ 'year' };

		# escape
		$city      =~ s/'/''/g;
		$date      =~ s/'/''/g;
		$extent    =~ s/'/''/g;
		$imprint   =~ s/'/''/g;
		$place     =~ s/'/''/g;
		$publisher =~ s/'/''/g;
		$title     =~ s/'/''/g;
		
		# initialize titles insert statement and do the work
		my $carrellhandle = $carrell->prepare( "INSERT INTO titles ( 'century', 'city', 'collection', 'date', 'extent', 'id', 'imprint', 'language', 'pages', 'place', 'publisher', 'title', 'words', 'year') VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );" ) or die $DBI::errstr;
		$carrellhandle->execute( $century, $city, $collection, $date, $extent, $id, $imprint, $language, $pages, $place , $publisher, $title, $words, $year ) or die $DBI::errstr;

		# find all authors for this item, and process each one
		my $subhandle = $dbh->prepare( "SELECT * FROM authors WHERE id='$id';" );
		$subhandle->execute() or die $DBI::errstr;
		while( my $authors = $subhandle->fetchrow_hashref ) {

			# parse
			my $collection = $$authors{ 'collection' };
			my $id         = $$authors{ 'id' };
			my $author     = $$authors{ 'author' };
			
			# escape
			$author =~ s/'/''/g;
			
			# initialize authors insert statement and do the work
			$carrellhandle = $carrell->prepare( "INSERT INTO authors ( 'collection', 'id', 'author') VALUES ( ?, ?, ? );" ) or die $DBI::errstr;
			$carrellhandle->execute( $collection, $id, $author ) or die $DBI::errstr;

		}
		
		
		# generate file names for plain text, entities and parts-of-speech
		my $txt = ROOT . &id2root( $collection, $id ) . "/$id.txt";
		my $ent = ROOT . &id2root( $collection, $id ) . "/$id.ent";
		my $pos = ROOT . &id2root( $collection, $id ) . "/$id.pos";
				
		# update the study carrel database with named entities and parts-of-speech
		&entities( $carrell, $ent );
		&pos( $carrell, $pos );
		
		# update the zip file
		$zip->addFile( $txt, "txt/$id.txt" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
		$zip->addFile( $ent, "ent/$id.ent" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
		$zip->addFile( $pos, "pos/$id.pos" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
		
	}
	
	# close the database connections
	$carrell->disconnect;
	$dbh->disconnect;

	# add the newly created study carrell database to the zip file
	$zip->addFile( CARRELLDB, "etc/carrell.db" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
	
	# save
	unless ( $zip->writeToFileNamed( ZIPFILE ) == AZ_OK ) { die "Can create " . ZIPFILE . " ($!). Error" }
	
	# done
	print $cgi->header;
	my $html = &results;
	print $html;

}

# done; whew, that was a lot of work
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


sub entities {

	# get input
	my $dbh  = shift;
	my $file = shift;
	
	# prepare the database
	my $sth = $dbh->prepare( "BEGIN TRANSACTION;" ) or die $DBI::errstr;
	$sth->execute or die $DBI::errstr;
	$sth = $dbh->prepare( "INSERT INTO entities ( 'id', 'sid', 'eid', 'entity', 'type' ) VALUES ( ?, ?, ?, ?, ? );" ) or die $DBI::errstr;

	# open the given file
	open FILE, " < $file" or die "Can't open $file ($!). Call Eric.\n";

	# process each line in the file
	my $counter = 0;
	while ( <FILE> ) {

		# increment; skip the first line
		$counter++;
		next if ( $counter == 1 );
	
		# parse, escape, and do the work
		chop;
		my ( $id, $sid, $eid, $entity, $type ) = split( "\t", $_ );
		$entity =~ s/'/''/g;
		$sth->execute( $id, $sid, $eid, $entity, $type ) or die $DBI::errstr;

	}
	
	# close the database
	$sth = $dbh->prepare( "END TRANSACTION;" ) or die $DBI::errstr;
	$sth->execute or die $DBI::errstr;

 }


sub pos {

	# get input
	my $dbh  = shift;
	my $file = shift;
	
	# prepare the database
	my $sth = $dbh->prepare( "BEGIN TRANSACTION;" ) or die $DBI::errstr;
	$sth->execute or die $DBI::errstr;
	$sth = $dbh->prepare( "INSERT INTO pos ( 'id', 'sid', 'tid', 'token', 'lemma', 'pos' ) VALUES ( ?, ?, ?, ?, ?, ? );" ) or die $DBI::errstr;

	# open the given file
	open FILE, " < $file" or die "Can't open $file ($!)\n";

	# process each line in the file
	my $counter = 0;
	while ( <FILE> ) {

		# increment; skip the first line
		$counter++;
		next if ( $counter == 1 );
	
		# parse, escape, and do the work
		chop;
		my ( $id, $sid, $tid, $token, $lemma, $pos ) = split( "\t", $_ );
		$token =~ s/'/''/g;
		$lemma =~ s/'/''/g;
		$sth->execute( $id, $sid, $tid, $token, $lemma, $pos ) or die $DBI::errstr;

	}
	
	# close the database
	$sth = $dbh->prepare( "END TRANSACTION;" ) or die $DBI::errstr;
	$sth->execute or die $DBI::errstr;

 }




