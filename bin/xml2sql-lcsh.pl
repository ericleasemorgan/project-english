#!/afs/crc.nd.edu/user/e/emorgan/bin/perl

# xml2sql-lcsh.pl - given an XML file as input, parse out LCSH as SQL INSERT statements

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame, distributed under a GNU Public License

# June 25, 2018 - first investigations
# June 26, 2018 - cleaned up and commented upon


# require
use strict;
use XML::XPath;
use XML::Parser;
use File::Basename;

# sanity check
my $collection = $ARGV[ 0 ];
my $file       = $ARGV[ 1 ];
if ( ! $file | ! $collection ) { &usage }
	
# initialize
my $parser   = XML::XPath->new( parser => XML::Parser->new( NoLWP => 1 ), filename => $file );
my $id       = basename( $file, ( '.xml' ) );
my @types    = ();
my @subjects = ();
my $headings = $parser->find( '/book/bookInfo/locSubjectHead' );

# process each found heading
while ( my $heading = $headings->pop ) {

	# extract the type of heading, just in case
	my $type = $heading->find( './@type' );
	push( @types, $type );

	# extract the headings themselves
	my @terms = ();
	my $terms = $heading->find( './locSubject' );
	while ( my $term = $terms->shift ) { push( @terms, $term->string_value ) }
	my $subject =  join( ' -- ', @terms );
	$subject    =~ s/'/''/g;
	push( @subjects, $subject );
	
}

# echo; debug
warn "        file: $file\n";
warn " colllection: $collection\n";
warn "          id: $id\n";
warn "     type(s): " . join( '; ', @types )    . "\n";
warn "  subject(s): " . join( '; ', @subjects ) . "\n";
warn "\n";
	
# output a comment and SQL DELETE statement insuring things are clean
print "-- file: $file\n";
print "DELETE FROM lcsh WHERE id='$id';\n";

# output SQL INSERT statements; assume each heading includes a type
my $pointer = -1;
foreach ( @types ) {

	$pointer++;
	my $type    = @types[ $pointer ];
	my $subject = @subjects[ $pointer ];
	print "INSERT INTO lcsh ( 'collection', 'id', 'type', 'subject' ) VALUES ( '$collection', '$id', '$type', '$subject' );\n"
	
}

# delimit and done
print "\n";
exit;


sub usage { die "Usage: $0 <freebo|ecco|sabin> <file>\n" }


