#!/afs/crc.nd.edu/user/e/emorgan/bin/perl

# xml2sql-term.pl - given an XML file as input, parse out the values of the "term" element

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame, distributed under a GNU Public License

# June 25, 2018 - first investigations


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
my @subjects = ();
my $subjects = $parser->find( '//term' );

# build a list of the subjects
while ( my $subject = $subjects->pop ) {

	my $term =  $subject->string_value;
	$term =~ s/'/''/g;
	push( @subjects, $term );
	
}

# echo
warn "        file: $file\n";
warn " colllection: $collection\n";
warn "          id: $id\n";
warn "  subject(s): " . join( '; ', @subjects ) . "\n";
warn "\n";
	
# output a comment and SQL statements
print "-- file: $file\n";
print "DELETE FROM lcsh WHERE id='$id';\n";
foreach my $subject ( @subjects ) { print "INSERT INTO lcsh ( 'collection', 'id', 'subject' ) VALUES ( '$collection', '$id', '$subject' );\n" }

# delimit and done
print "\n";
exit;

sub usage { die "Usage: $0 <freebo|ecco|sabin> <file>\n" }


