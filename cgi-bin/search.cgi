#!/usr/bin/perl

# search.cgi - CGI interface to search a solr instance

# Eric Lease Morgan <emorgan@nd.edu>
# November  7, 2016
# January   4, 2017 - tweaked
# February 24, 2017 - modified where to find full text version(s)
# March     7, 2017 - added subject facets and snippets
# March     8, 2017 - faceted on many things; can you say, "creeping featuritis"? 
# March     9, 2017 - added ability to download tsv of search results metadata
# July     19, 2017 - beginning to add styling; at the cabin!


# configure
use constant HOME           => 'http://cds.crc.nd.edu/';
use constant FACETFIELD     => ( 'facet_author', 'facet_collection', 'facet_language', 'facet_city', 'facet_century', 'facet_year' );
use constant FIELDS         => 'id,collection,title,author,imprint,extent';
use constant FREEBO         => '/collections/freebo';
use constant ECCO           => '/collections/ecco';
use constant SABIN          => '/collections/sabin';
use constant ROWS           => 199;
use constant SOLR           => 'http://localhost:8983/solr/english';

# require
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use HTML::Entities;
use strict;
use WebService::Solr;
use URI::Encode qw(uri_encode uri_decode);

# initialize
my $cgi   = CGI->new;
my $query = $cgi->param( 'query' );
my $html  = &template;
my $solr  = WebService::Solr->new( SOLR );

# sanitize query
my $sanitized = HTML::Entities::encode($query);

# display the home page
if ( ! $query ) {

	$html =~ s/##QUERY##//;
	$html =~ s/##RESULTS##//;

}

# search
else {

	# re-initialize
	my $items = '';
	my @ids  = ();
	
	# build the search options
	my %search_options                   = ();
	$search_options{ 'facet.field' }     = [ FACETFIELD ];
	$search_options{ 'facet' }           = 'true';
	$search_options{ 'rows' }            = ROWS;
	$search_options{ 'fl' }              = FIELDS;

	# search
	my $response = $solr->search( $query, \%search_options );

	# build a list of author facets
	my @facets_author = ();
	my $author_facets = &get_facets( $response->facet_counts->{ facet_fields }->{ facet_author } );
	foreach my $facet ( sort { $$author_facets{ $b } <=> $$author_facets{ $a } } keys %$author_facets ) {
	
		my $encoded = uri_encode( $facet );
		my $link = qq(<a href='/cgi-bin/search.cgi?query=$sanitized AND author:"$encoded"'>$facet</a>);
		push @facets_author, $link . ' (' . $$author_facets{ $facet } . ')';
		
	}

	# build a list of collection facets
	my @facets_collection = ();
	my $collection_facets = &get_facets( $response->facet_counts->{ facet_fields }->{ facet_collection } );
	foreach my $facet ( sort { $$collection_facets{ $b } <=> $$collection_facets{ $a } } keys %$collection_facets ) {
	
		my $link = qq(<a href='/cgi-bin/search.cgi?query=$sanitized AND collection:"$facet"'>$facet</a>);
		push @facets_collection, $link . ' (' . $$collection_facets{ $facet } . ')';
		
	}

	# build a list of language facets
	my @facets_year = ();
	my $year_facets = &get_facets( $response->facet_counts->{ facet_fields }->{ facet_year } );
	foreach my $facet ( sort { $$year_facets{ $b } <=> $$year_facets{ $a } } keys %$year_facets ) {
	
		my $link = qq(<a href='/cgi-bin/search.cgi?query=$sanitized AND year:"$facet"'>$facet</a>);
		push @facets_year, $link . ' (' . $$year_facets{ $facet } . ')';
		
	}

	# build a list of language facets
	my @facets_language = ();
	my $language_facets = &get_facets( $response->facet_counts->{ facet_fields }->{ facet_language } );
	foreach my $facet ( sort { $$language_facets{ $b } <=> $$language_facets{ $a } } keys %$language_facets ) {
	
		my $link = qq(<a href='/cgi-bin/search.cgi?query=$sanitized AND language:"$facet"'>$facet</a>);
		push @facets_language, $link . ' (' . $$language_facets{ $facet } . ')';
		
	}

	# build a list of language facets
	my @facets_century = ();
	my $century_facets = &get_facets( $response->facet_counts->{ facet_fields }->{ facet_century } );
	foreach my $facet ( sort { $$century_facets{ $b } <=> $$century_facets{ $a } } keys %$century_facets ) {
	
		my $link = qq(<a href='/cgi-bin/search.cgi?query=$sanitized AND century:"$facet"'>) . $facet . 'th</a>';
		push @facets_century, $link . ' (' . $$century_facets{ $facet } . ')';
		
	}

	# build a list of language facets
	my @facets_city = ();
	my $city_facets = &get_facets( $response->facet_counts->{ facet_fields }->{ facet_city } );
	foreach my $facet ( sort { $$city_facets{ $b } <=> $$city_facets{ $a } } keys %$city_facets ) {
	
		my $link = qq(<a href='/cgi-bin/search.cgi?query=$sanitized AND city:"$facet"'>$facet</a>);
		push @facets_city, $link . ' (' . $$city_facets{ $facet } . ')';
		
	}

	# build a list of language facets
	my @facets_date = ();
	my $date_facets = &get_facets( $response->facet_counts->{ facet_fields }->{ facet_date } );
	foreach my $facet ( sort { $$date_facets{ $b } <=> $$date_facets{ $a } } keys %$date_facets ) {
	
		my $link = qq(<a href='/cgi-bin/search.cgi?query=$sanitized AND date:"$facet"'>$facet</a>);
		push @facets_date, $link . ' (' . $$date_facets{ $facet } . ')';
		
	}

	# get the total number of hits
	my $total = $response->content->{ 'response' }->{ 'numFound' };

	# get number of hits
	my @hits = $response->docs;

	# loop through each document
	for my $doc ( $response->docs ) {
	
		# parse
		my $collection = $doc->value_for( 'collection' );
		my $id         = $doc->value_for( 'id' );
		my $title      = $doc->value_for( 'title' );
		my $extent     = $doc->value_for( 'extent' );
		my $imprint    = $doc->value_for( 'imprint' );

		# update the list of dids
		push(@ids, $id );
				
		# build a path to the details
		my $details = '';
		if ( $collection eq 'freebo' ) { 
		
			my $prefix  = substr( $id, 0, 3 );
			$details = FREEBO . "/$prefix/$id/";
			
		}
		
		if ( $collection eq 'sabin' ) { 
		
			my $prefix  = substr( $id, 3, 3 ) . '/' . substr( $id, 6, 3 );
			$details = SABIN . "/$prefix/$id/";
			
		}
		
		if ( $collection eq 'ecco' ) { 
		
			my $prefix  = substr( $id, 0, 2 ) . '/' . substr( $id, 2, 2 );
			$details = ECCO . "/$prefix/$id/";
			
		}
			
		my @authors = ();
		foreach my $author ( $doc->values_for( 'author' ) ) {
		
			my $author = qq(<a href='/cgi-bin/search.cgi?query=author:"$author"'>$author</a>);
			push( @authors, $author );

		}

		# create a cool list of authors, a la catalog cards
		my $authors = '';
		for ( my $i = 0; $i < scalar( @authors ); $i++ ) { $authors .= $i +1 . '. ' . @authors[ $i ] . ' ' }
		
		# create a item
		my $item = &item( $imprint, $extent, scalar( @authors ) );
		$item =~ s/##TITLE##/$title/g;
		$item =~ s/##AUTHORS##/$authors/eg;
		$item =~ s/##DETAILS##/$details/e;
		$item =~ s/##ID##/$id/e;
		$item =~ s/##IMPRINT##/$imprint/e;
		$item =~ s/##EXTENT##/$extent/e;

		# update the list of items
		$items .= $item;
					
	}	

	# populate forms
	my $id2tsv =  &ids2tsv;
	$id2tsv    =~ s/##IDS##/join( ' ', @ids )/e;
	my $id2table =  &ids2table;
	$id2table    =~ s/##IDS##/join( ' ', @ids )/e;
	my $id2zip =  &ids2zip;
	$id2zip    =~ s/##IDS##/join( ' ', @ids )/e;

	# build the html
	$html =  &results_template;
	$html =~ s/##RESULTS##/&results/e;
	$html =~ s/##ID2TSV##/$id2tsv/ge;
	$html =~ s/##ID2TABLE##/$id2table/ge;
	$html =~ s/##ID2ZIP##/$id2zip/ge;
	$html =~ s/##QUERY##/$sanitized/e;
	$html =~ s/##TOTAL##/$total/e;
	$html =~ s/##HITS##/scalar( @hits )/e;
	$html =~ s/##FACETSCOLLECTION##/join( '; ', @facets_collection )/e;
	$html =~ s/##FACETSLANGUAGE##/join( '; ', @facets_language )/e;
	$html =~ s/##FACETSCITY##/join( '; ', @facets_city )/e;
	$html =~ s/##FACETSDATE##/join( '; ', @facets_date )/e;
	$html =~ s/##FACETSCENTURY##/join( '; ', @facets_century )/e;
	$html =~ s/##FACETSYEAR##/join( '; ', @facets_year )/e;
	$html =~ s/##FACETSAUTHOR##/join( '; ', @facets_author )/e;
	$html =~ s/##ITEMS##/$items/e;

}

# done
print $cgi->header( -type => 'text/html', -charset => 'utf-8');
print $html;
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


# search results template
sub results {

	return <<EOF
	<p>Your search found ##TOTAL## item(s) and ##HITS## item(s) are displayed.</p>
	
	<p>##ID2TABLE## | ##ID2TSV## | ##ID2ZIP##</p>
	
	<h3>Items</h3><ol>##ITEMS##</ol>
EOF

}


# specific item template
sub item {

	my $imprint = shift;
	my $extent  = shift;
	my $authors = shift;
	my $item    = "<li class='item'>##TITLE## (<a href='##DETAILS##'>##ID##</a>)<ul>";
	
	if ( $imprint ) { $item .= "<li style='list-style-type:circle'>##IMPRINT##</li>" }
	if ( $extent )  { $item .= "<li style='list-style-type:circle'>##EXTENT##</li>" }
	
	$item .= "</ul>";
	
	if ( $authors ) { $item .= "##AUTHORS##" }
	
	$item .= "</li>";
	
	return $item;

}


# root template
sub template {

	return <<EOF
<html>
<head>
	<title>Project English</title>
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link rel="stylesheet" href="/etc/style.css">
	<style>
		.item { margin-bottom: 1em }
	</style>
</head>
<body>
<div class="header">
	<h1>English - Search</h1>
</div>

<div class="col-3 col-m-3 menu">
  <ul>
    <li><a href="/home.html">Home</a></li>
    <li><a href="/about/">About and scope</a></li>
	<li><a href="/cgi-bin/search.cgi">Search</a></li>
 </ul>
</div>

<div class="col-9 col-m-9">

	<p>Given a query, this page will return a relevancy ranked list of results.</p>
	<p>
	<form method='GET' action='./search.cgi'>
	<input type='text' name='query' value='##QUERY##' size='50' />
	<input type='submit' value='Search' />
	</form>

<p>Or search by Great Idea: <a href='/cgi-bin/search.cgi?query=title:angel'>angel</a>, <a href='/cgi-bin/search.cgi?query=title:animal'>animal</a>, <a href='/cgi-bin/search.cgi?query=title:aristocracy'>aristocracy</a>, <a href='/cgi-bin/search.cgi?query=title:art'>art</a>, <a href='/cgi-bin/search.cgi?query=title:astronomy'>astronomy</a>, <a href='/cgi-bin/search.cgi?query=title:beauty'>beauty</a>, <a href='/cgi-bin/search.cgi?query=title:being'>being</a>, <a href='/cgi-bin/search.cgi?query=title:cause'>cause</a>, <a href='/cgi-bin/search.cgi?query=title:chance'>chance</a>, <a href='/cgi-bin/search.cgi?query=title:change'>change</a>, <a href='/cgi-bin/search.cgi?query=title:citizen'>citizen</a>, <a href='/cgi-bin/search.cgi?query=title:constitution'>constitution</a>, <a href='/cgi-bin/search.cgi?query=title:contingency'>contingency</a>, <a href='/cgi-bin/search.cgi?query=title:convention'>convention</a>, <a href='/cgi-bin/search.cgi?query=title:cosmology'>cosmology</a>, <a href='/cgi-bin/search.cgi?query=title:courage'>courage</a>, <a href='/cgi-bin/search.cgi?query=title:custom'>custom</a>, <a href='/cgi-bin/search.cgi?query=title:death'>death</a>, <a href='/cgi-bin/search.cgi?query=title:definition'>definition</a>, <a href='/cgi-bin/search.cgi?query=title:democracy'>democracy</a>, <a href='/cgi-bin/search.cgi?query=title:desire'>desire</a>, <a href='/cgi-bin/search.cgi?query=title:despotism'>despotism</a>, <a href='/cgi-bin/search.cgi?query=title:dialectic'>dialectic</a>, <a href='/cgi-bin/search.cgi?query=title:duty'>duty</a>, <a href='/cgi-bin/search.cgi?query=title:education'>education</a>, <a href='/cgi-bin/search.cgi?query=title:element'>element</a>, <a href='/cgi-bin/search.cgi?query=title:emotion'>emotion</a>, <a href='/cgi-bin/search.cgi?query=title:equality'>equality</a>, <a href='/cgi-bin/search.cgi?query=title:eternity'>eternity</a>, <a href='/cgi-bin/search.cgi?query=title:evil'>evil</a>, <a href='/cgi-bin/search.cgi?query=title:evolution'>evolution</a>, <a href='/cgi-bin/search.cgi?query=title:experience'>experience</a>, <a href='/cgi-bin/search.cgi?query=title:family'>family</a>, <a href='/cgi-bin/search.cgi?query=title:fate'>fate</a>, <a href='/cgi-bin/search.cgi?query=title:form'>form</a>, <a href='/cgi-bin/search.cgi?query=title:god'>god</a>, <a href='/cgi-bin/search.cgi?query=title:good'>good</a>, <a href='/cgi-bin/search.cgi?query=title:government'>government</a>, <a href='/cgi-bin/search.cgi?query=title:habit'>habit</a>, <a href='/cgi-bin/search.cgi?query=title:happiness'>happiness</a>, <a href='/cgi-bin/search.cgi?query=title:history'>history</a>, <a href='/cgi-bin/search.cgi?query=title:honor'>honor</a>, <a href='/cgi-bin/search.cgi?query=title:hypothesis'>hypothesis</a>, <a href='/cgi-bin/search.cgi?query=title:idea'>idea</a>, <a href='/cgi-bin/search.cgi?query=title:imagination'>imagination</a>, <a href='/cgi-bin/search.cgi?query=title:immortality'>immortality</a>, <a href='/cgi-bin/search.cgi?query=title:induction'>induction</a>, <a href='/cgi-bin/search.cgi?query=title:infinity'>infinity</a>, <a href='/cgi-bin/search.cgi?query=title:judgment'>judgment</a>, <a href='/cgi-bin/search.cgi?query=title:justice'>justice</a>, <a href='/cgi-bin/search.cgi?query=title:knowledge'>knowledge</a>, <a href='/cgi-bin/search.cgi?query=title:labor'>labor</a>, <a href='/cgi-bin/search.cgi?query=title:language'>language</a>, <a href='/cgi-bin/search.cgi?query=title:law'>law</a>, <a href='/cgi-bin/search.cgi?query=title:liberty'>liberty</a>, <a href='/cgi-bin/search.cgi?query=title:life'>life</a>, <a href='/cgi-bin/search.cgi?query=title:logic'>logic</a>, <a href='/cgi-bin/search.cgi?query=title:love'>love</a>, <a href='/cgi-bin/search.cgi?query=title:man'>man</a>, <a href='/cgi-bin/search.cgi?query=title:many'>many</a>, <a href='/cgi-bin/search.cgi?query=title:mathematics'>mathematics</a>, <a href='/cgi-bin/search.cgi?query=title:matter'>matter</a>, <a href='/cgi-bin/search.cgi?query=title:mechanics'>mechanics</a>, <a href='/cgi-bin/search.cgi?query=title:medicine'>medicine</a>, <a href='/cgi-bin/search.cgi?query=title:memory'>memory</a>, <a href='/cgi-bin/search.cgi?query=title:metaphysics'>metaphysics</a>, <a href='/cgi-bin/search.cgi?query=title:mind'>mind</a>, <a href='/cgi-bin/search.cgi?query=title:monarchy'>monarchy</a>, <a href='/cgi-bin/search.cgi?query=title:nature'>nature</a>, <a href='/cgi-bin/search.cgi?query=title:necessity'>necessity</a>, <a href='/cgi-bin/search.cgi?query=title:oligarchy'>oligarchy</a>, <a href='/cgi-bin/search.cgi?query=title:one'>one</a>, <a href='/cgi-bin/search.cgi?query=title:opinion'>opinion</a>, <a href='/cgi-bin/search.cgi?query=title:opposition'>opposition</a>, <a href='/cgi-bin/search.cgi?query=title:other'>other</a>, <a href='/cgi-bin/search.cgi?query=title:pain'>pain</a>, <a href='/cgi-bin/search.cgi?query=title:particular'>particular</a>, <a href='/cgi-bin/search.cgi?query=title:peace'>peace</a>, <a href='/cgi-bin/search.cgi?query=title:philosophy'>philosophy</a>, <a href='/cgi-bin/search.cgi?query=title:physics'>physics</a>, <a href='/cgi-bin/search.cgi?query=title:pleasure'>pleasure</a>, <a href='/cgi-bin/search.cgi?query=title:poetry'>poetry</a>, <a href='/cgi-bin/search.cgi?query=title:principle'>principle</a>, <a href='/cgi-bin/search.cgi?query=title:progress'>progress</a>, <a href='/cgi-bin/search.cgi?query=title:prophecy'>prophecy</a>, <a href='/cgi-bin/search.cgi?query=title:prudence'>prudence</a>, <a href='/cgi-bin/search.cgi?query=title:punishment'>punishment</a>, <a href='/cgi-bin/search.cgi?query=title:quality'>quality</a>, <a href='/cgi-bin/search.cgi?query=title:quantity'>quantity</a>, <a href='/cgi-bin/search.cgi?query=title:reasoning'>reasoning</a>, <a href='/cgi-bin/search.cgi?query=title:relation'>relation</a>, <a href='/cgi-bin/search.cgi?query=title:religion'>religion</a>, <a href='/cgi-bin/search.cgi?query=title:revolution'>revolution</a>, <a href='/cgi-bin/search.cgi?query=title:rhetoric'>rhetoric</a>, <a href='/cgi-bin/search.cgi?query=title:same'>same</a>, <a href='/cgi-bin/search.cgi?query=title:science'>science</a>, <a href='/cgi-bin/search.cgi?query=title:sense'>sense</a>, <a href='/cgi-bin/search.cgi?query=title:sign'>sign</a>, <a href='/cgi-bin/search.cgi?query=title:sin'>sin</a>, <a href='/cgi-bin/search.cgi?query=title:slavery'>slavery</a>, <a href='/cgi-bin/search.cgi?query=title:soul'>soul</a>, <a href='/cgi-bin/search.cgi?query=title:space'>space</a>, <a href='/cgi-bin/search.cgi?query=title:state'>state</a>, <a href='/cgi-bin/search.cgi?query=title:symbol'>symbol</a>, <a href='/cgi-bin/search.cgi?query=title:temperance'>temperance</a>, <a href='/cgi-bin/search.cgi?query=title:theology'>theology</a>, <a href='/cgi-bin/search.cgi?query=title:time'>time</a>, <a href='/cgi-bin/search.cgi?query=title:truth'>truth</a>, <a href='/cgi-bin/search.cgi?query=title:tyranny'>tyranny</a>, <a href='/cgi-bin/search.cgi?query=title:universal'>universal</a>, <a href='/cgi-bin/search.cgi?query=title:vice'>vice</a>, <a href='/cgi-bin/search.cgi?query=title:virtue'>virtue</a>, <a href='/cgi-bin/search.cgi?query=title:war'>war</a>, <a href='/cgi-bin/search.cgi?query=title:wealth'>wealth</a>, <a href='/cgi-bin/search.cgi?query=title:will'>will</a>, <a href='/cgi-bin/search.cgi?query=title:wisdom'>wisdom</a>, <a href='/cgi-bin/search.cgi?query=title:world'>world</a></p>


	##RESULTS##

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


# results template
sub results_template {

	return <<EOF
<html>
<head>
	<title>Project English</title>
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link rel="stylesheet" href="/etc/style.css">
	<style>
		.item { margin-bottom: 1em }
	</style>
</head>
<body>
<div class="header">
	<h1>Project English - Search results</h1>
</div>

<div class="col-3 col-m-3 menu">
	<ul>
		<li><a href="/home.html">Home</a></li>
		<li><a href="/about/">About and scope</a></li>
		<li><a href="/cgi-bin/search.cgi">Search</a></li>
	</ul>
</div>

	<div class="col-6 col-m-6">
		<p>
		<form method='GET' action='/cgi-bin/search.cgi'>
		<input type='text' name='query' value='##QUERY##' size='50' />
		<input type='submit' value='Search' />
		</form>
		
		
		##RESULTS##
		
	</div>
	
	<div class="col-3 col-m-3">
	<h3>Collection facets</h3><p>##FACETSCOLLECTION##</p>
	<h3>Language facets</h3><p>##FACETSLANGUAGE##</p>
	<h3>Century facets</h3><p>##FACETSCENTURY##</p>
	<h3>Year facets</h3><p>##FACETSYEAR##</p>
	<h3>Author facets</h3><p>##FACETSAUTHOR##</p>
	<h3>Publication city facets</h3><p>##FACETSCITY##</p>
	<!-- <h3>Date facets</h3><p>##FACETSDATE##</p> -->
	</div>

</body>
</html>
EOF

}

sub ids2tsv {

	return <<EOF
<a href="/cgi-bin/ids2tsv.cgi?ids=##IDS##">Download metadata</a>
EOF

}

sub ids2table {

	return <<EOF
<a href="/cgi-bin/ids2table.cgi?ids=##IDS##">View as table</a>
EOF

}

sub ids2zip {

	return <<EOF
<a href="/cgi-bin/ids2zip.cgi?ids=##IDS##">Download search results</a>
EOF

}




