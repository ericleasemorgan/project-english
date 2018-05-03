#!/afs/crc.nd.edu/user/e/emorgan/bin/perl

# xml2sql.pl - given an XML file as input, parse out bibliographic data, and output SQL INSERT statements

# Eric Lease Morgan <emorgan@nd.edu>
# December 21, 2017 - first investigations
# December 23, 2017 - started adding authors
# April    13, 2018 - changed INSERT statements to UPDATE statements; smart
# April    15, 2018 - added year and century, kewl; at the cabin
# May       1, 2018 - added extent and imprint for each collection


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
my $bibliographics = '';
if    ( $collection eq 'freebo' ) { $bibliographics = &freebo( $parser ) }
elsif ( $collection eq 'ecco' )   { $bibliographics = &ecco( $parser ) }
elsif ( $collection eq 'sabin' )  { $bibliographics = &sabin( $parser ) }
else  { &usage }

# read
my $date      = $$bibliographics{ 'date' };
my $year      = &date2year( $date );
my $city      = &normalizeCity( $$bibliographics{ 'place' } );
my $century   = &date2century( $year );
my $extent    = $$bibliographics{ 'extent' };
my $language  = $$bibliographics{ 'language' };
my $pages     = $$bibliographics{ 'pages' };
my $place     = $$bibliographics{ 'place' };
my $publisher = $$bibliographics{ 'publisher' };
my $imprint   = $$bibliographics{ 'imprint' };
my $title     = $$bibliographics{ 'title' };
my $words     = $$bibliographics{ 'words' };

# sql escape single quote marks; gotta be an easier way
$extent    =~ s/'/''/g;
$publisher =~ s/'/''/g;
$title     =~ s/'/''/g;
$place     =~ s/'/''/g;
$city      =~ s/'/''/g;
$date      =~ s/'/''/g;
$imprint   =~ s/'/''/g;

# echo
warn "        file: $file\n";
warn "  collection: $collection\n";
warn "          id: $id\n";
warn "        city: $city\n";
warn "     century: $century\n";
warn "        date: $date\n";
warn "      extent: $extent\n";
warn "     imprint: $imprint\n";
warn "    language: $language\n";
warn "       pages: $pages\n";
warn "       place: $place\n";
warn "   publisher: $publisher\n";
warn "       title: $title\n";
warn "       words: $words\n";
warn "        year: $year\n";
warn "\n";
	
# output comment and SQL statements
print "-- file: $file\n";
print "UPDATE titles SET city='$city', century='$century', collection='$collection', date='$date', extent='$extent', imprint='$imprint', language='$language', pages='$pages', place='$place', publisher='$publisher', title='$title', words='$words', year='$year' WHERE id='$id';\n";
print "\n";

# done
exit;


sub normalizeCity {

	my $city = shift;
	
	$city =~ s/\[//g;
	$city =~ s/\]//g;
	$city =~ s/\?//g;
	$city =~ s/\://g;
	$city =~ s/At //g;
	$city =~ s/Ann Arbor, Michigan//g;
	$city =~ s/Printed at //g;
	$city =~ s/Printed in //g;
	$city =~ s/Imprinted at //g;
	$city =~ s/Londini/London/g;
	$city =~ s/Londres/London/g;
	$city =~ s/New-York/New York/g;
	$city =~ s/ Ohio//g;
	$city =~ s/ Conn//g;
	$city =~ s/ Calif//g;
	$city =~ s/ England//g;
	$city =~ s/, England//g;
	$city =~ s/^\W+//g;
	$city =~ s/\W+$//g;
	
	return $city;
	
}


sub normalizeLanguage {

	my $l = shift;
	warn "$l\n";
	if ( $l eq "eng" ) { $l = "Eric was here."; }
		
	return $l;
	
}


sub date2year {

	my $date = shift;
	my $year = '';
	
	# brute force substitution
	$date =~ s/\D//g;
	
	if ( $date =~ /^\d\d\d\d$/ ) { $year = $date }

	return $year;
	
}


sub date2century {

	my $date    = shift;
	my $century = '';
	
	if ( $date =~ /^\d\d\d\d$/ ) { $century = substr( $date, 0, 2) + 1  }
	
	return $century;
	
}


sub usage { die "Usage: $0 <freebo|ecco|sabin> <file>\n" }


sub freebo {

	# initialize
	my $parser         = shift;
	my %bibliographics = {};
	
	# parse the easy stuff
	my $language  = $parser->find( '/TEI/teiHeader/profileDesc/langUsage/language' );
	my $pages     = $parser->find( '//pb' )->size;
	my $title     = $parser->find( '/TEI/teiHeader/fileDesc/titleStmt/title' )->string_value;
	my $words     = $parser->find( '//w' )->size;

	# initialize for the hard stuff
	my $extent    = '';
	my $place     = '';
	my $publisher = '';
	my $date      = '';
	
	# parse TCP weirdness
	if ( $parser->find( '/TEI/teiHeader/fileDesc/sourceDesc/biblFull[@n="printed source"]' ) ) {
	
		$extent    = $parser->find( '/TEI/teiHeader/fileDesc/sourceDesc/biblFull[@n="printed source"]/extent' );
		$place     = $parser->find( '/TEI/teiHeader/fileDesc/sourceDesc/biblFull[@n="printed source"]/publicationStmt/pubPlace' );
		$publisher = $parser->find( '/TEI/teiHeader/fileDesc/sourceDesc/biblFull[@n="printed source"]/publicationStmt/publisher' );
		
		if ( $parser->find( '/TEI/teiHeader/fileDesc/sourceDesc/biblFull[@n="printed source"]/publicationStmt/date[@type="publication_date"]' ) ) {
		
			$date = $parser->find( '/TEI/teiHeader/fileDesc/sourceDesc/biblFull[@n="printed source"]/publicationStmt/date[@type="publication_date"]' );
			
		}
		
		else {
		
			$date =  $parser->find( '/TEI/teiHeader/fileDesc/sourceDesc/biblFull[@n="printed source"]/publicatinoStmt/date' );
		
		}
		

	}		
	
	# no weirdness
	else {
	
		$extent    = $parser->find( '/TEI/teiHeader/fileDesc/sourceDesc/biblFull/extent' );
		$place     = $parser->find( '/TEI/teiHeader/fileDesc/sourceDesc/biblFull/publicationStmt/pubPlace' );
		$publisher = $parser->find( '/TEI/teiHeader/fileDesc/sourceDesc/biblFull/publicationStmt/publisher' );
		$date      = $parser->find( '/TEI/teiHeader/fileDesc/sourceDesc/biblFull/publicationStmt/date' );

	}
	
	# update
	$bibliographics{ 'date' }      = $date;
	$bibliographics{ 'extent' }    = $extent;
	$bibliographics{ 'language' }  = $language;
	$bibliographics{ 'pages' }     = $pages;
	$bibliographics{ 'place' }     = $place;
	$bibliographics{ 'imprint' }   = "$place $publisher $date";
	$bibliographics{ 'publisher' } = $publisher;
	$bibliographics{ 'title' }     = $title;
	$bibliographics{ 'words' }     = $words;
	
	# done
	return \%bibliographics;

}


sub ecco {

	# initialize
	my $parser         = shift;
	my %bibliographics = {};
	
	# parse
	my $date      = $parser->find( '/book/citation/imprint/imprintYear' );
	my $extent    = $parser->find( '/book/citation/collation' );
	my $imprint   = $parser->find( '/book/citation/imprint/imprintFull' );
	my $language  = $parser->find( '/book/bookInfo/language' );
	my $pages     = $parser->find( '//page' )->size;
	my $place     = $parser->find( '/book/citation/imprint/imprintCity' );
	my $publisher = $parser->find( '/book/citation/imprint/imprintPublisher' );
	my $title     = $parser->find( '/book/citation/titleGroup/fullTitle' );
	my $words     = $parser->find( '//wd' )->size;
	
	# update
	$bibliographics{ 'date' }      = $date;
	$bibliographics{ 'extent' }    = $extent;
	$bibliographics{ 'imprint' }   = $imprint;
	$bibliographics{ 'language' }  = $language;
	$bibliographics{ 'pages' }     = $pages;
	$bibliographics{ 'place' }     = $place;
	$bibliographics{ 'publisher' } = $publisher;
	$bibliographics{ 'title' }     = $title;
	$bibliographics{ 'words' }     = $words;
	
	# done
	return \%bibliographics;

}


sub sabin {

	# initialize
	my $parser         = shift;
	my %bibliographics = {};
	
	# parse
	my $date      = $parser->find( '/book/citation/imprint/imprintYear' );
	my $extent    = $parser->find( '/book/citation/collation' );
	my $imprint   = $parser->find( '/book/citation/imprint/imprintFull' );
	my $language  = $parser->find( '/book/bookInfo/language' );
	my $pages     = $parser->find( '//page' )->size;
	my $place     = $parser->find( '/book/citation/imprint/imprintCity' );
	my $publisher = $parser->find( '/book/citation/imprint/imprintPublisher' );
	my $title     = $parser->find( '/book/citation/titleGroup/fullTitle' );
	my $words     = $parser->find( '//wd' )->size;
	
	# update
	$bibliographics{ 'date' }      = $date;
	$bibliographics{ 'extent' }    = $extent;
	$bibliographics{ 'imprint' }   = $imprint;
	$bibliographics{ 'language' }  = $language;
	$bibliographics{ 'pages' }     = $pages;
	$bibliographics{ 'place' }     = $place;
	$bibliographics{ 'publisher' } = $publisher;
	$bibliographics{ 'title' }     = $title;
	$bibliographics{ 'words' }     = $words;
	
	# done
	return \%bibliographics;

}

