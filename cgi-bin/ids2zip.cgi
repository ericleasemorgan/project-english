#!/usr/bin/perl

# ids2zip.cgi - given one more more identifiers, create a zip file of content for downloading

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# April 19, 2018 - first investigations; need to fill out README, etc.
# June   6, 2018 - added some scripts as well as ent & pos files
# June   8, 2018 - added title, author, entity, and pos data to database while at ELAG 2018; jeesh!


# configure
use constant CARRELLDB       => '../tmp/carrell.db';
use constant CARRELLSQL      => '../etc/carrell.sql';
use constant CLUSTER         => '../etc/search-results/bin/cluster.py';
use constant ASSERT          => '../etc/search-results/bin/assert.sh';
use constant DESCRIBE        => '../etc/search-results/bin/describe.sh';
use constant DESCRIBES       => '../etc/search-results/bin/describe-sequentially.sh';
use constant DRIVER          => 'SQLite';
use constant LICENSE         => '../etc/search-results/LICENSE';
use constant MANIFEST        => '../etc/search-results/MANIFEST';
use constant MODEL           => '../etc/search-results/bin/model.py';
use constant NGRAMS          => '../etc/search-results/bin/ngrams.py';
use constant NOUNPHRASES     => '../etc/search-results/bin/noun-phrases.py';
use constant README          => '../etc/search-results/README';
use constant ROOT            => '..';
use constant STOPWORDS       => '../etc/search-results/etc/stopwords.txt';
use constant SUMMARIZE       => '../etc/search-results/bin/summarize.sh';
use constant WHATISDESCRIBED => '../etc/search-results/bin/what-is-described-as.sh';
use constant WHATISOBJECT    => '../etc/search-results/bin/what-is-the-object-of.sh';
use constant WHATWASDONE     => '../etc/search-results/bin/what-was-done-by.sh';
use constant ZIPFILE         => '../tmp/search-results.zip';

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
	my @ids = ();
	
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
	$zip->addFile( CLUSTER, "bin/cluster.py" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
	$zip->addFile( ASSERT, "bin/assert.sh" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
	$zip->addFile( DESCRIBE, "bin/describe.sh" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
	$zip->addFile( DESCRIBES, "bin/describe-sequentially.sh" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
	$zip->addFile( MODEL, "bin/model.py" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
	$zip->addFile( NGRAMS, "bin/ngrams.py" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
	$zip->addFile( NOUNPHRASES, "bin/noun-phrases.py" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
	$zip->addFile( SUMMARIZE, "bin/summarize.sh" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
	$zip->addFile( WHATWASDONE, "bin/what-was-done-by.sh" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
	$zip->addFile( WHATISOBJECT, "bin/what-is-the-object-of.sh" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
	$zip->addFile( WHATWASDONE, "bin/what-was-done-by.sh" )->desiredCompressionMethod( COMPRESSION_DEFLATED );

	# create etc directory and add... stuff
	$zip->addDirectory( 'etc/' );
	$zip->addFile( STOPWORDS, "etc/stopwords.txt" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
	
	# create directories for content
	$zip->addDirectory( 'txt/' );
	$zip->addDirectory( 'ent/' );
	$zip->addDirectory( 'pos/' );

	# delete, open, and initialize a study carrell database
	unlink( ( CARRELLDB ) );
	my $database = CARRELLDB;
	my $driver   = DRIVER;
	my $carrell  = DBI->connect( "DBI:$driver:dbname=$database", '', '', { RaiseError => 1 } ) or die $DBI::errstr;
	foreach my $statement ( split ";", &slurp( CARRELLSQL ) ) { $carrell->do( $statement ) }

	# open a connect to the master database
	my $english = &connect2db;

	# process each of the given ids
	foreach my $id ( @ids ) {

		# given the id, find its collection
		my $handle = $english->prepare( "SELECT collection FROM titles WHERE id IS '$id'" );
		$handle->execute() or die $DBI::errstr;
 		my $collection = $handle->fetchrow_array();
 		
		# generate file names for plain text, entities and parts-of-speech
		my $txt = ROOT . &id2root( $collection, $id ) . "/$id.txt";
		my $ent = ROOT . &id2root( $collection, $id ) . "/$id.ent";
		my $pos = ROOT . &id2root( $collection, $id ) . "/$id.pos";
		my $db  = ROOT . &id2root( $collection, $id ) . "/$id.db";
		
		$carrell->do( qq( ATTACH "$db" AS 'item'; ) );
		$carrell->do( qq( INSERT INTO titles   SELECT * FROM item.titles   WHERE id IS '$id'; ) );
		$carrell->do( qq( INSERT INTO authors  SELECT * FROM item.authors  WHERE id IS '$id'; ) );
		$carrell->do( qq( INSERT INTO pos      SELECT * FROM item.pos      WHERE id IS '$id'; ) );
		$carrell->do( qq( INSERT INTO entities SELECT * FROM item.entities WHERE id IS '$id'; ) );
		$carrell->do( qq( DETACH DATABASE 'item'; ) );

		# update the zip file
		$zip->addFile( $txt, "txt/$id.txt" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
		$zip->addFile( $ent, "ent/$id.ent" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
		$zip->addFile( $pos, "pos/$id.pos" )->desiredCompressionMethod( COMPRESSION_DEFLATED );

	}
	
	# close the database connections
	$carrell->disconnect;
	$english->disconnect;

	# add the newly created study carrell database to the zip file and save
	$zip->addFile( CARRELLDB, "etc/carrell.db" )->desiredCompressionMethod( COMPRESSION_DEFLATED );
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
    <li><a href="/about/">About</a></li>
    <li><a href="/cgi-bin/search.cgi">Search</a></li>
    <li><a href="/tools.html">Extra tools</a></li>
 </ul>
</div>

<div class="col-9 col-m-9">

<p>Done. You can now <a href='/tmp/search-results.zip'>download a zip file of your search results</a>.</p>

<p>The linked zip file contains plain text files, an SQLite database, and a few scripts/programs written in Bash or Python. In order to take advantage of the download, you probably don't any additional software since your computer can probably already open/read the plain text files with your text editor and/or spreadsheet program. On the other hand, you will be able to get more out of the download if you also install additional pieces of software:</p>

<ul>
	<li><a href="http://openrefine.org">OpenRefine</a> - useful for reading &amp; analyzing the named-entity and parts-of-speech files; better than your spreadsheet, I promise</li>
	<li><a href="http://www.laurenceanthony.net/software/antconc/">AntConc</a> - a concordance ("keyword-in-context") application for "reading" the plain text versions of the items in the corpus; very very useful but requires practice</li>
	<li><a href="https://github.com/senderle/topic-modeling-tool">topic-modeling-tool</a> - sub-divides the items in the downloads into smaller collections based on "topics"</li>
	<li><a href="https://www.sqlite.org/">SQLite</a> - a cross-platform relational database program</li>
	<li><a href="https://anaconda.org/anaconda/python">Python</a> - a popular programming language which may already be on your computer but may reqiure additional modules to be installed</li>
</ul>
<p>Thank you for using Project English.</p>

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
    <li><a href="/about/">About</a></li>
    <li><a href="/cgi-bin/search.cgi">Search</a></li>
    <li><a href="/tools.html">Extra tools</a></li>
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
