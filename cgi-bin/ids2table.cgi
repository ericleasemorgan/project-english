#!/usr/bin/perl

# id2table.cgi - given one more more identifiers, output a human-readable table

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame; distributed under a GNU Public License

# April 18, 2017 - first investigations; based on work from Early Print
# April 28, 2017 - added authors


# configure
use constant QUERY => qq(SELECT * FROM titles WHERE ##CLAUSE## ORDER BY title;);

# require
use strict;
use CGI;
require '/afs/crc.nd.edu/user/e/emorgan/local/english/lib/english.pl';

# initialize
my $cgi     = CGI->new;
my $ids    = $cgi->param( 'ids' );

# no input; display home page
if ( ! $ids ) {

	print $cgi->header;
	my $html = &form;
	print $html;
	
}

# process input
else {

	# initialize
	my @ids     = ();
	my @queries = ();
	my %records = ();
	
	# get input and sanitize it
	$ids =~ s/[[:punct:]]/ /g;
	$ids =~ s/ +/ /g;
	@ids =  split( ' ', $ids );

	# VALIDATE INPUT HERE; we don't need to leave an opportunity for sql injection!

	# create the sql where clause and then build the whole sql query
	for my $id ( @ids ) { push( @queries, "id='$id'" ) }
	my $sql =  QUERY;
	$sql    =~ s/##CLAUSE##/join( ' OR ', @queries )/e;

	# execute the query
	my $dbh    = &connect2db;
	my $handle = $dbh->prepare( $sql );
	$handle->execute() or die $DBI::errstr;

	# process each title in the found set
	while( my $titles = $handle->fetchrow_hashref ) {
	
		my %record         = ();

		# parse the title data
		my $city       = $$titles{ 'city' };
		my $collection = $$titles{ 'collection' };
		my $language   = $$titles{ 'language' };
		my $id         = $$titles{ 'id' };
		my $pages      = $$titles{ 'pages' };
		my $place      = $$titles{ 'place' };
		my $publisher  = $$titles{ 'publisher' };
		my $title      = $$titles{ 'title' };
		my $words      = $$titles{ 'words' };
		my $year       = $$titles{ 'year' };
		my $extent     = $$titles{ 'extent' };
		my $date       = $$titles{ 'date' };

		my $link = &id2root( $collection, $id );

		# find the given title's authors; only get the first one
		my $author = '';
		my $subhandle = $dbh->prepare( qq(SELECT * FROM authors WHERE id='$id';) );
		$subhandle->execute() or die $DBI::errstr;
		my $results = $subhandle->fetchrow_hashref;
		$author     = $$results{ 'author' };
		
		# debug; dump
		warn "       identifier: $id\n";
		warn "           author: $author\n";
		warn "            title: $title\n";
		warn "        publisher: $publisher $place $date\n";
		warn "           extent: $extent\n";
		warn "             city: $city\n";
		warn "             year: $year\n";
		warn "            pages: $pages\n";
		warn "            words: $words\n";
		warn "             link: $link\n";
		warn "\n";

		# create a record and then update the "database"
		%record = ( 'author' => $author, 'title' => $title, 'publisher' => $publisher, 'city' => $city, 'place' => $place, 'date' => $date, 'extent' => $extent, 'pages' => $pages, 'words' => $words, 'link' => $link, 'collection' => $collection, 'language' => $language, 'extent' => $extent, 'year' => $year );
		$records{ $id } = \%record;
	
	}

	# process each record, sorted by author
	my $tbody = '';
	foreach ( sort { $records{ $b }->{ 'author' } <=> $records{ $a }->{'author'} } keys %records ) { 
			
		# parse
		my $id         = $_;
		my $record     = $records{ $id };	
		my $author     = $$record{ 'author' };
		my $title      = $$record{ 'title' };
		my $date       = $$record{ 'date' };
		my $year       = $$record{ 'year' };
		my $publisher  = $$record{ 'publisher' };
		my $place      = $$record{ 'place' };
		my $city       = $$record{ 'city' };
		my $pages      = $$record{ 'pages' };
		my $collection = $$record{ 'collection' };
		my $language   = $$record{ 'language' };
		my $words      = $$record{ 'words' };
		my $link       = $$record{ 'link' };
				
		my $details = '<li>Extent: ' . $$record{ 'extent' } . '</li>';
		$details    = "<ul>$details</ul>";

		# build a row
		my $row  = "<td style='vertical-align:top'><a href='$link'>$id</a></td>";
		$row    .= "<td style='vertical-align:top'>$author</td>";
		$row    .= "<td style='vertical-align:top'>$title</td>";
		$row    .= "<td style='vertical-align:top'>$collection</td>";
		$row    .= "<td style='vertical-align:top'>$language</td>";
		$row    .= "<td style='vertical-align:top'>$year</td>";
		$row    .= "<td style='vertical-align:top'>$city</td>";
		$row    .= "<td style='vertical-align:top'>$pages</td>";
		$row    .= "<td style='vertical-align:top'>$words</td>";
		
		# update the table
		$tbody .= "<tr>$row</tr>";

	}

	# populate forms
	my $id2tsv =  &ids2tsv;
	$id2tsv    =~ s/##IDS##/join( ' ', @ids )/e;
	
	# finish the table
	$tbody   =  "<tbody>$tbody</tbody>";
	my $html =  &db2table;
	$html    =~ s/##ID2TSV##/$id2tsv/ge;
	$html    =~ s/##TBODY##/$tbody/;

	print $cgi->header( -type => 'text/html', -charset => 'utf-8');
	print $html;

}


# done
exit;


sub form {

	return <<EOF
<html>
<head>
<title>Project English</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="/etc/style.css">
</head>
<body>
<div class="header">
	<h1>Project English - View as table</h1>
</div>

<div class="col-3 col-m-3 menu">
  <ul>
    <li><a href="/home.html">Home</a></li>
    <li><a href="/about/">About and scope</a></li>
	<li><a href="/cgi-bin/search.cgi">Search</a></li>
 </ul>
</div>

<div class="col-9 col-m-9">

<p>Given a set of one more more Project English identifiers, this page will return a tabled view of the set. This enables the reader to sort their search results in any number of ways.</p>
<form method='POST' action='/cgi-bin/ids2table.cgi'>
<input type='text' name='ids' size='50' value='1302901107 1323300900 1323600600 1346000200 1375900300 A07517 A08185 A66057 A67873 A67917 SABCPA8064301 SABCPA8094100 SABCPA8098400 SABCPA8193404 SABCPA8258500'/>
<input type='submit' value='View as table' />
</form>

<div class="footer">

<p style='text-align: right'>
Eric Lease Morgan &amp; Team Project English<br />
April 18, 2018
</p>

</div>

</div>


</body>
</html>
EOF
	
}


sub db2table {

	return <<EOF;
<!DOCTYPE html>
<head>
	<title>Project English - View as table</title>
  	<script type="text/javascript" charset="utf8" src="/etc/jquery-3.0.0.min.js"></script>
	<script type="text/javascript" charset="utf8" src="/etc/DataTables/datatables.js"></script>
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link rel="stylesheet" href="/etc/style.css">
	<link rel="stylesheet" type="text/css" href="/etc/DataTables/datatables.css">
    <script>
		\$(document).ready(function() { 
			\$('#bibliographics').DataTable({"order": [[ 1, "asc" ]], "paging": false });
		});
  	</script>
</head>
<body>

<h1>Project English - View as table</h1>

<p>##ID2TSV##</p>

<table id="bibliographics" class="display" cellspacing="0" width="100%">
        <thead>
            <tr>
				<th>Identifier</th>
				<th>Author</th>
				<th>Title</th>
				<th>Collection</th>
				<th>Language</th>
				<th>Year</th>
				<th>City</th>
				<th>Pages</th>
				<th>Words</th>
            </tr>
        </thead>
        <tfoot>
            <tr>
				<th>Identifier</th>
				<th>Author</th>
				<th>Title</th>
				<th>Collection</th>
				<th>Language</th>
				<th>Year</th>
				<th>City</th>
				<th>Pages</th>
				<th>Words</th>
            </tr>
        </tfoot>
		##TBODY##
    </table>
</body>
</html>
EOF
}

sub ids2tsv {

	return <<EOF
<a href="/cgi-bin/ids2tsv.cgi?ids=##IDS##">Download metadata</a>
EOF

}



