#!/usr/bin/perl

# id2html.pl - given an identifier, create an HTML pages

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame, distributed under a GNU Public License

# April 23, 2018 - first investigations
# May 9, 2018    - added log-likelihood


# configure
use constant COLLECTIONS => '/afs/crc.nd.edu/user/e/emorgan/local/english/collections';
use constant TEMPLATE    => '/afs/crc.nd.edu/user/e/emorgan/local/english/etc/template-html.txt';

# require
use DBI;
use strict;
require '/afs/crc.nd.edu/user/e/emorgan/local/english/lib/english.pl';

# sanity check
my $key = $ARGV[ 0 ];
if ( ! $key ) { die "Usage: $0 <key>\n" }

# find the given title
my $dbh    = &connect2db;
my $handle = $dbh->prepare( qq(SELECT * FROM titles WHERE id='$key';) );
$handle->execute() or die $DBI::errstr;
my $results = $handle->fetchrow_hashref;

# parse the title data
my $collection = $$results{ 'collection' };
my $extent     = $$results{ 'extent' };
my $id         = $$results{ 'id' };
my $place      = $$results{ 'place' };
my $date       = $$results{ 'date' };
my $publisher  = $$results{ 'publisher' };
my $title      = $$results{ 'title' };
my $pages      = $$results{ 'pages' };
my $words      = $$results{ 'words' };
my $century    = $$results{ 'century' };
my $language   = $$results{ 'language' };

if ( ! $collection ) { die "Unknown value for collection ($collection) in record $id. Call Eric.\n" }

my $fullpath = &id2root( $collection, $id );

# debug; dump
warn "  collection: $collection\n";
warn "    fullpath: $fullpath\n";
warn "          id: $id\n";
warn "        date: $date\n";
warn "      extent: $extent\n";
warn "       place: $place\n";
warn "   publisher: $publisher\n";
warn "       title: $title\n";
warn "       pages: $pages\n";
warn "       words: $words\n";
warn "     century: $century\n";
warn "    language: $language\n";
warn "\n";

$title     = &escape( $title );
$publisher = &escape( $publisher );
$extent    = &escape( $extent );
$date      = &escape( $date );

my $html = &slurp( TEMPLATE );
$html =~ s/##TITLE##/$title/g;
$html =~ s/##EXTENT##/$extent/g;
$html =~ s/##PLACE##/$place/g;
$html =~ s/##PUBLISHER##/$publisher/g;
$html =~ s/##FULLPATH##/$fullpath/g;
$html =~ s/##ID##/$id/g;
$html =~ s/##DATE##/$date/g;
$html =~ s/##PAGES##/$pages/g;
$html =~ s/##WORDS##/$words/g;
$html =~ s/##COLLECTION##/$collection/g;
$html =~ s/##CENTURY##/$century/g;
$html =~ s/##LANGUAGE##/$language/g;

print $html;

# done
exit;

