#!/usr/bin/perl

# index.pl - make the content searchable

# Eric Lease Morgan <emorgan@nd.edu>
# December 26, 2017 - first cut
# April    15, 2017 - migrating to Project English, big time


# configure
use constant DATABASE    => './etc/english.db';
use constant DRIVER      => 'SQLite';
use constant SOLR        => 'http://localhost:8983/solr/english';
use constant COLLECTIONS => '/afs/crc.nd.edu/user/e/emorgan/local/english/collections';

# require
use DBI;
use strict;
use WebService::Solr;

# sanity check
my $key = $ARGV[ 0 ];
if ( ! $key ) { die "Usage: $0 <key>\n" }

# initialize
my $driver   = DRIVER; 
my $database = DATABASE;
my $dbh      = DBI->connect( "DBI:$driver:dbname=$database", '', '', { RaiseError => 1 } ) or die $DBI::errstr;

# find the given title
my $handle = $dbh->prepare( qq(SELECT * FROM titles WHERE id='$key';) );
$handle->execute() or die $DBI::errstr;
my $results = $handle->fetchrow_hashref;

# parse the title data
my $city       = $$results{ 'city' };
my $century    = $$results{ 'century' };
my $collection = $$results{ 'collection' };
my $date       = $$results{ 'date' };
my $extent     = $$results{ 'extent' };
my $id         = $$results{ 'id' };
my $imprint    = $$results{ 'imprint' };
my $language   = $$results{ 'language' };
my $pages      = $$results{ 'pages' };
my $place      = $$results{ 'place' };
my $publisher  = $$results{ 'publisher' };
my $title      = $$results{ 'title' };
my $words      = $$results{ 'words' };
my $year       = $$results{ 'year' };

my $fulltext = '';
my $fullpath = '';

if ( $collection eq 'freebo' ) {

	my $code  = substr( $id, 0, 3);
	$fullpath = COLLECTIONS . "/freebo/$code/$id/$id.txt";
	$fulltext = &slurp( $fullpath );
	
}
elsif ( $collection eq 'ecco' ) { 

	my $code  = substr( $id, 0, 2 ) . '/' . substr( $id, 2, 2 );
	$fullpath = COLLECTIONS . "/ecco/$code/$id/$id.txt";
	$fulltext = &slurp( $fullpath );
	
}

elsif ( $collection eq 'sabin' ) { 

	my $code  = substr( $id, 3, 3 ) . '/' . substr( $id, 6, 3 );
	$fullpath = COLLECTIONS . "/sabin/$code/$id/$id.txt";
	$fulltext = &slurp( $fullpath );

}
else { die "Unknown value for collection ($collection) in record $id. Call Eric.\n" }

# find the given title's authors
my @authors = ();
my $handle = $dbh->prepare( qq(SELECT * FROM authors WHERE id='$key';) );
$handle->execute() or die $DBI::errstr;
while( my $results = $handle->fetchrow_hashref ) { push( @authors, $$results{ 'author' } ) }

# debug; dump
binmode( STDOUT, ':utf8' );
warn "        city: $city\n";
warn "  collection: $collection\n";
warn "    fullpath: $fullpath\n";
warn "          id: $id\n";
warn "     imprint: $imprint\n";
warn "        date: $date\n";
warn "      extent: $extent\n";
warn "    language: $language\n";
warn "       pages: $pages\n";
warn "       place: $place\n";
warn "   publisher: $publisher\n";
warn "       title: $title\n";
warn "       words: $words\n";
warn "        year: $year\n";
warn "     century: $century\n";
warn "   author(s): " . join( '; ', @authors ) . "\n";
warn "\n";

# initialize indexing
my $solr                  = WebService::Solr->new( SOLR );
my $solr_collection       = WebService::Solr::Field->new( 'collection'       => $collection );
my $solr_facet_collection = WebService::Solr::Field->new( 'facet_collection' => $collection );
my $solr_facet_date       = WebService::Solr::Field->new( 'facet_date'       => $date );
my $solr_facet_language   = WebService::Solr::Field->new( 'facet_language'   => $language );
my $solr_facet_century    = WebService::Solr::Field->new( 'facet_century'    => $century );
my $solr_facet_year       = WebService::Solr::Field->new( 'facet_year'       => $year );
my $solr_facet_language   = WebService::Solr::Field->new( 'facet_language'   => $language );
my $solr_facet_city       = WebService::Solr::Field->new( 'facet_city'       => $city );
my $solr_fulltext         = WebService::Solr::Field->new( 'fulltext'         => $fulltext );
my $solr_id               = WebService::Solr::Field->new( 'id'               => $id );
my $solr_imprint          = WebService::Solr::Field->new( 'imprint'          => $imprint );
my $solr_date             = WebService::Solr::Field->new( 'date'             => $date );
my $solr_extent           = WebService::Solr::Field->new( 'extent'           => $extent );
my $solr_language         = WebService::Solr::Field->new( 'language'         => $language );
my $solr_pages            = WebService::Solr::Field->new( 'pages'            => $pages );
my $solr_place            = WebService::Solr::Field->new( 'place'            => $place );
my $solr_city             = WebService::Solr::Field->new( 'city'             => $city );
my $solr_publisher        = WebService::Solr::Field->new( 'publisher'        => $publisher );
my $solr_title            = WebService::Solr::Field->new( 'title'            => $title );
my $solr_words            = WebService::Solr::Field->new( 'words'            => $words );
my $solr_century          = WebService::Solr::Field->new( 'century'          => $century );
my $solr_year             = WebService::Solr::Field->new( 'year'             => $year );

# fill a solr document with simple fields
my $doc = WebService::Solr::Document->new;
$doc->add_fields( $solr_collection, $solr_facet_collection, $solr_facet_date, $solr_facet_year, $solr_facet_century, $solr_facet_language, $solr_facet_city, $solr_fulltext, $solr_id, $solr_imprint, $solr_city, $solr_date, $solr_extent, $solr_language, $solr_pages, $solr_place, $solr_publisher, $solr_title, $solr_year, $solr_century,
$solr_words );

# add complex fields
foreach ( @authors ) {

	$doc->add_fields(( WebService::Solr::Field->new( 'author'       => $_ )));
	$doc->add_fields(( WebService::Solr::Field->new( 'facet_author' => $_ )));
	
}


# save/index
$solr->add( $doc );

# done
exit;


sub slurp {

	my $f = shift;
	open ( F, $f ) or die "Can't open $f: $!\n";
	my $r = do { local $/; <F> };
	close F;
	return $r;

}

