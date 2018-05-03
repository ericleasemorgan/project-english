#!/usr/bin/env perl

# search.pl - command-line interface to search a solr instance

# Eric Lease Morgan <emorgan@nd.edu>
# October 20, 2017 - first cut; based on earlier work
# April    4, 2018 - working with amalgamated collections


# configure
use constant FACETFIELD         => ( 'facet_author' );
use constant HIGHLIGHTDELIMITER => '*';
use constant HIGHLIGHTFEILD     => 'fulltext';
use constant ROWS               => 10;
use constant SNIPPETS           => 3;
use constant SOLR               => 'http://localhost:8983/solr/english';

# require
use strict;
use WebService::Solr;

# get input; sanity check
my $query = $ARGV[ 0 ];
if ( ! $query ) { die "Usage: $0 <query>\n" }

# initialize
my $solr = WebService::Solr->new( SOLR );

# build the search options
my %search_options = ();
$search_options{ 'facet.field' }    = [ FACETFIELD ];
$search_options{ 'facet' }          = 'true';
$search_options{ 'hl.fl' }          = HIGHLIGHTFEILD;
$search_options{ 'hl.simple.post' } = HIGHLIGHTDELIMITER;
$search_options{ 'hl.simple.pre' }  = HIGHLIGHTDELIMITER;
$search_options{ 'hl.snippets' }    = SNIPPETS;
$search_options{ 'hl' }             = 'true';
$search_options{ 'rows' }           = ROWS;

# search
my $response = $solr->search( $query, \%search_options );

# build a list of collection facets
my @facets_author = ();
my $author_facets = &get_facets( $response->facet_counts->{ facet_fields }->{ facet_author } );
foreach my $facet ( sort { $$author_facets{ $b } <=> $$author_facets{ $a } } keys %$author_facets ) { push @facets_author, $facet . ' (' . $$author_facets{ $facet } . ')'; }

# get highlights
my $highlights = $response->content->{ 'highlighting' };

# get the total number of hits
my $total = $response->content->{ 'response' }->{ 'numFound' };

# get number of hits returned
my @hits = $response->docs;

# start the output
print "Your search found $total item(s) and " . scalar( @hits ) . " items(s) are displayed.\n\n";
print '  author facets: ', join( '; ', @facets_author ), "\n\n";

# loop through each document
for my $doc ( $response->docs ) {
	
	# parse
	my $collection = $doc->value_for(  'collection' );
	my $id         = $doc->value_for(  'id' );
	my $title      = $doc->value_for(  'title' );
	my @authors    = $doc->values_for(  'author' );
			
	# create a list of snippets
	my @snippets = ();
	for ( my $i = 0; $i < SNIPPETS; $i++ ) {
	
		my $snippet  =  $highlights->{ $id }->{ fulltext }->[ $i ];
		$snippet     =~ s/\s+/ /g;
		$snippet     =~ s/^ +//;
		push( @snippets, $snippet );
		
	}
		
	# output
	print "  collection: $collection\n";
	print "          id: $id\n";
	print "       title: $title\n";
	print "   author(s): " . join( '; ', @authors ) . "\n";
	print "     snippet: " . join( ' ... ', @snippets ), "\n";
	print "\n";
	
}

# done
exit;


# convert an array reference into a hash
sub get_facets {

	my $array_ref = shift;
	
	my %facets;
	my $i = 0;
	foreach ( @$array_ref ) {
	
		my $k = $array_ref->[ $i ]; $i++;
		my $v = $array_ref->[ $i ]; $i++;
		next if ( ! $v );
		$facets{ $k } = $v;
	 
	}
	
	return \%facets;
	
}


