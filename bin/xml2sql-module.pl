#!/afs/crc.nd.edu/user/e/emorgan/bin/perl

# xml2sql-module.pl - given an XML file as input, parse out the values of the "module" element

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
my $parser= XML::XPath->new( parser => XML::Parser->new( NoLWP => 1 ), filename => $file );
#binmode( STDOUT, ':utf8' );
#binmode( STDERR, ':utf8' );

# create an identifier
my $id = basename( $file, ( '.xml' ) );

# parse easy stuff
my @modules = ();
my $modules = $parser->find( '/book/bookInfo/module' );
while ( my $module = $modules->pop ) { push( @modules, $module->string_value ) }

# echo
warn "        file: $file\n";
warn " colllection: $collection\n";
warn "          id: $id\n";
warn "   module(s): " . join( '; ', @modules ) . "\n";
warn "\n";
	
# output a comment and SQL statements
print "-- file: $file\n";
print "DELETE FROM modules WHERE id='$id';\n";
foreach my $module ( @modules ) { print "INSERT INTO modules ( 'collection', 'id', 'module' ) VALUES ( '$collection', '$id', '$module' );\n" }
print "\n";

# done
exit;

sub usage { die "Usage: $0 <freebo|ecco|sabin> <file>\n" }

