#!/afs/crc.nd.edu/user/e/emorgan/bin/perl

# xml2sql-authors.pl - given an XML file as input, parse out author data, and output SQL UPDATE statements

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame, distributed under a GNU Public License

# April 27, 2018 - first investigations; not too hard


# require
use strict;
use XML::XPath;
use XML::Parser;
use File::Basename;

# sanity check
my $collection = $ARGV[ 0 ];
my $file       = $ARGV[ 1 ];
if ( ! $file | ! $collection ) { &usage; }
	
# initialize
my $parser= XML::XPath->new( parser => XML::Parser->new( NoLWP => 1 ), filename => $file );
binmode( STDOUT, ':utf8' );
binmode( STDERR, ':utf8' );

# create an identifier
my $id = basename( $file, ( '.xml' ) );

# parse easy stuff
my $authors = '';
if    ( $collection eq 'freebo' ) { $authors = &freebo( $parser ) }
elsif ( $collection eq 'ecco' )   { $authors = &ecco( $parser ) }
elsif ( $collection eq 'sabin' )  { $authors = &sabin( $parser ) }
else  { &usage }

# initialize, read, and escape each author
my @authors = ();
my $authors = $$authors{ 'authors' };
foreach my $author ( @$authors ) {

	$author =~ s/'/''/g;
	push( @authors, $author );
	
}

# echo
warn "        file: $file\n";
warn "  collection: $collection\n";
warn "          id: $id\n";
warn "   author(s): " . join( '; ', @authors ) . "\n";
warn "\n";
	
# no need to continue, if there are no authors
#exit if ( scalar( @authors ) == 0 );

# output a comment and SQL statements
print "-- file: $file\n";
print "DELETE FROM authors WHERE id='$id';\n";
foreach my $author ( @authors ) { print "INSERT INTO authors ( 'collection', 'id', 'author' ) VALUES ( '$collection', '$id', '$author' );\n" }
print "\n";

# done
exit;


sub usage { die "Usage: $0 <freebo|ecco|sabin> <file>\n" }



sub freebo {

	# initialize
	my $parser  = shift;
	my %authors = {};
	my @authors = ();
	
	# parse
	my $authors = $parser->find( '/TEI/teiHeader/fileDesc/sourceDesc/biblFull/titleStmt/author' );
	while ( my $author = $authors->pop ) { push( @authors, $author->string_value ) }
	
	# remove duplicates
	my %seen = {};
	@authors = grep( ! $seen{ $_ }++, @authors );

	# update and done
	$authors{ 'authors' } = \@authors;
	return \%authors;

}



sub ecco {

	# initialize
	my $parser  = shift;
	my %authors = {};
	my @authors = ();
	
	# parse
	my $entries = $parser->find( '/book/citation/authorGroup/author/marcName' );
	while ( my $author = $entries->pop ) { push( @authors, $author->string_value ) }
	$authors{ 'authors' } = \@authors;
	return \%authors;

}


sub sabin {

	# initialize
	my $parser  = shift;
	my %authors = {};
	my @authors = ();
	
	# parse
	my $entries = $parser->find( '/book/citation/authorGroup/author/marcName' );
	while ( my $author = $entries->pop ) { push( @authors, $author->string_value ) }
	$authors{ 'authors' } = \@authors;
	return \%authors;

}

