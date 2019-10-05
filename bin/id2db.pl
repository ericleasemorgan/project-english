#!/usr/bin/perl

# id2db.pl - given a directory name, create an sqlite database

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame, distributed under a GNU Public License

# June 12, 2018 - first investigations


# configure
use constant CARRELLSQL => '/afs/crc.nd.edu/user/e/emorgan/local/html/english/etc/carrell.sql';
use constant DRIVER     => 'SQLite';
use constant ENGLISH    => '/afs/crc.nd.edu/user/e/emorgan/local/html/english/etc/english.db';

# require
use DBI;
use strict;
require '/afs/crc.nd.edu/user/e/emorgan/local/html/english/lib/english.pl';

# sanity check
my $directory = $ARGV[ 0 ];
if ( ! $directory ) { die "Usage: $0 <directory>\n" }

# change the working directory
chdir $directory or die "Can't change directory ($!). Call Eric.\n";

# based on the directory name (id), initialize the database
my @paths    = split( /\//, $directory );
my $id       = $paths[ $#paths ];
my $driver   = DRIVER;
my $database = "$id.db";
unlink( ( $database ) );
my $carrell  = DBI->connect( "DBI:$driver:dbname=$database", '', '', { RaiseError => 1 } ) or die $DBI::errstr;
foreach my $statement ( split ";", &slurp( CARRELLSQL ) ) { $carrell->do( $statement ) }

# attach to the master database, and fill our new one with content
my $english = ENGLISH;
$carrell->do( qq( ATTACH "$english" AS english; ) );
$carrell->do( qq( INSERT INTO titles  SELECT * FROM english.titles  WHERE id IS '$id'; ) );
$carrell->do( qq( INSERT INTO authors SELECT * FROM english.authors WHERE id IS '$id'; ) );
&entities( $carrell, "$id.ent" );
&pos( $carrell, "$id.pos" );

# done
exit;


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






