#!/usr/bin/env perl

# ner2tab.pl - given an XML file of a specific shape, output a tab-delimited file of named entitites

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame under a GNU Public License

# April 10, 2018 - first documentation; getting closer to Prague
# May   12, 2018 - migrating/enhancing for Project English; added identifier column


# configure
use constant HEADER => ( 'id', 'type', 'entity' );
use constant NODES  => "//LOCATION|//PERSON|//ORGANIZATION|//DATE|//TIME|//MONEY|//PERCENT";

# require
use File::Basename;
use strict;
use XML::XPath;
  
# get input
my $xml = $ARGV[ 0 ];

# do error checking here

# generate an identifier from the file name
my ( $id, $path, $suffix ) = fileparse( $xml, ( '.xml' ) );

# initialize output, do the work, and done
print join( "\t", HEADER ), "\n";
print &ner2tab( $id, $xml );
exit;


# the hardest work is done here; extract specific XML entities
sub ner2tab {

	# initialize
	my $id     = shift;
	my $xml    = shift;
	my $result = '';
	my $ner    = XML::XPath->new( filename => $xml );

	# process the desired elements
	foreach my $entity ( $ner->findnodes( NODES )->get_nodelist ) {

		# parse and build up the result
		my $type   = $entity->getName;
		my $entity = $entity->string_value;
		$result   .= join( "\t", ( $id, $type, $entity ) ) . "\n";
	
	}
	
	# done
	return $result;

}

