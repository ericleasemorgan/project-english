#!/usr/bin/perl

# likelihood.cgi - given two collection identifiers, compute the log-likelihood (G2) value for the words in the analysis text

# Eric Lease Morgan <emorgan@nd.edu>
# (c) University of Notre Dame, distributed under a GNU Public License

# May 8, 2018 - based on Early Print work
# May 9, 2018 - added stop words

# configure
use constant VERBOSE   => 0;
use constant STOPWORDS => '../etc/stopwords-en.txt';

# require
use strict;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
require '/afs/crc.nd.edu/user/e/emorgan/local/english/lib/english.pl';

# initialize
my $cgi          = CGI->new;
my $analysis_id  = $cgi->param( 'analysis_id' );
my $reference_id = $cgi->param( 'reference_id' );
my $html         = '';

# check for input
if ( ! $analysis_id | ! $reference_id ) {

	$html =  &template;
	$html =~ s/##CONTENT##/&home/e }

# process the input
else {

	# initialize
	my $stopwords = &stopwords( STOPWORDS );
	foreach my $word ( keys %$stopwords ) { warn "$word\n" if VERBOSE }
	
	# count the total number of words in the analysis text (c)
	my $dbh    = &connect2db;
	my $handle = $dbh->prepare( qq( SELECT words AS c FROM titles WHERE id='$analysis_id'; ) );
	my $result = $handle->execute() or die $DBI::errstr;
	my $row    = $handle->fetchrow_hashref();
	my $c      = $$row{ 'c' };
	print STDERR "Total number of words in $analysis_id: $c\n" if VERBOSE;

	# count the total number of words in the reference text (d)
	$handle = $dbh->prepare( qq( SELECT words AS d FROM titles WHERE id='$reference_id'; ) );
	$result = $handle->execute() or die $DBI::errstr;
	$row    = $handle->fetchrow_hashref();
	my $d   = $$row{ 'd' };
	print STDERR "Total number of words in $reference_id: $d\n" if VERBOSE;

	# determine the collection of analysis text
	$handle = $dbh->prepare( qq( SELECT collection FROM titles WHERE id='$analysis_id'; ) );
	$result = $handle->execute() or die $DBI::errstr;
	$row    = $handle->fetchrow_hashref();
	my $collection = $$row{ 'collection' };
	
	# get the full text of the analysis text, normalize it, and create a list of all the words
	my $analysis =  lc( &slurp( '..' . &id2root( $collection, $analysis_id ) . "/$analysis_id.txt" ) );
	$analysis    =~ s/ +/\n/g;
	$analysis    =~ s/[[:punct:]]$//g;
	$analysis    =~ s/\n+/ /g;
	my @analysis = split( ' ', $analysis );
	my %analysis = ();
	foreach my $analysis ( @analysis ) {
		next if $$stopwords{ $analysis };
		next if $analysis =~ /[[:punct:]]$/;
		next if $analysis =~ /^[[:punct:]]/;
		$analysis{ $analysis }++
	}
	print STDERR keys( %analysis ) if VERBOSE;
	
	# do the same thing for the reference text; determine the collection
	$handle     = $dbh->prepare( qq( SELECT collection FROM titles WHERE id='$reference_id'; ) );
	$result     = $handle->execute() or die $DBI::errstr;
	$row        = $handle->fetchrow_hashref();
	$collection = $$row{ 'collection' };
	
	# get and normalize the reference text, and then create a list of all words
	my $reference =  lc( &slurp( '..' . &id2root( $collection, $reference_id ) . "/$reference_id.txt" ) );
	$reference    =~ s/ +/\n/g;
	$reference    =~ s/[[:punct:]]$//g;
	$reference    =~ s/\n+/ /g;
	my @reference = split( ' ', $reference );
	my %reference = ();
	foreach my $reference ( @reference ) { 
		next if $$stopwords{ $reference };
		next if $reference =~ /[[:punct:]]$/;
		next if $reference =~ /^[[:punct:]]/;
		$reference{ $reference }++
	}
	print STDERR keys( %reference ) if VERBOSE;
		
	# process each reference text word to build up likelihood ratios
	my %likelihoods  = ();
	foreach my $word ( keys %reference ) {
	
		# re-initialize
		my %record            = ( 'relative use' => 0, 'g2' => 0, 'analysis count' => '', 'reference count' => '' );
		$likelihoods{ $word } = \%record;
	
		# count the number of times a reference word appears in the analysis text (a)
		my $a = $analysis{ $word };
	
		# sometimes a word does not appear in the text
		next if ( ! $a );
	
		# count the number of times the given word appears in the reference text (b)
		my $b = $reference{ $word };

		# do the work; compute G2
		my $e1 = $c * ( $a + $b ) / ( $c + $d );
		my $e2 = $d * ( $a + $b ) / ( $c + $d );
		my $g2 = sprintf( "%.3f", ( 2 * ( ( $a * log( $a / $e1 ) ) + ( $b * log( $b / $e2 ) ) ) ) );

		# echo
		print STDERR "$word = $g2\n" if VERBOSE;
	
		# calculate parts / 10,000 and relative use
		my $reference_parts = sprintf( "%.3f", ( $b * 10000 ) / $d );
		my $analysis_parts  = sprintf( "%.3f", ( $a * 10000 ) / $c );
		my $relative_use    = 1;
		if ( $analysis_parts < $reference_parts ) { $relative_use = -1 }
	
		# update likelihood
		%record = ( 'relative use' => $relative_use, 'g2' => $g2, 'analysis count' => $a, 'reference count' => $b, 'analysis parts' => $analysis_parts, 'reference parts' => $reference_parts );
		$likelihoods{ $word } = \%record;
	
	}

	# process each word, sorted by likelihood
	my $tbody = '';
	foreach ( sort { $likelihoods{ $b }->{ 'relative use' } <=> $likelihoods{ $a }->{'relative use'} or ( $likelihoods{ $b }->{ 'g2' } <=> $likelihoods{ $a }->{ 'g2' } ) } keys %likelihoods ) { 
			
		# parse
		my $word            = $_;
		my $record          = $likelihoods{ $word };	
		my $relative_use    = $$record{ 'relative use' };
		my $g2              = $$record{ 'g2' };
		my $analysis_count  = $$record{ 'analysis count' };
		my $reference_count = $$record{ 'reference count' };
		my $analysis_parts  = $$record{ 'analysis parts' };
		my $reference_parts = $$record{ 'reference parts' };

		# build a row
		my $row  = "<td style='text-align: center'>$word</td>";
		$row    .= "<td style='text-align: center'>$relative_use</td>";
		$row    .= "<td style='text-align: center'>$g2</td>";
		$row    .= "<td style='text-align: center'>$analysis_count</td>";
		$row    .= "<td style='text-align: center'>$reference_count</td>";
		$row    .= "<td style='text-align: center'>$analysis_parts</td>";
		$row    .= "<td style='text-align: center'>$reference_parts</td>";
		
		# update the table
		$tbody .= "<tr>$row</tr>";

	}
	
		# finish the table
		$tbody = "<tbody>$tbody</tbody>";
		$html  =  &db2table;
		$html  =~ s/##TBODY##/$tbody/;
		$html  =~ s/##TITLE##/$analysis_id/eg;

}

# output & done
print $cgi->header;
print $html;
exit;


sub result {

	return <<EOF
<p>These are the Log-likelihood ratios for the "great ideas" found in TCP identifer ##DID##. In other words, this service answers the question, "Relative to a set of 100 great ideas, what are the emphases of this particular text?"</p>
<p><img align='right' src='./tmp/cloud.png' /></p>
<table cellpadding='2'>
##ROWS##
</table>
EOF

}


sub home {

	return <<EOF
<p>Given two Project English identifiers, this form will return the log-likelihood ratio (G2) for all the words in first document of the given identifiers. Words with higher G2 ratio are more significant for the first document when compared to the second. Words with lower G2 ratio are less significant. Log-likelihood ratios help answer questions like, "What is significant in this text but not the other? How can I characterize this text? What are some of this text's more unique qualities? What make it different?" The following form will compare &amp; contrast Shakespeare's <cite>Hamlet</cite> with the same author's <cite>The Merry Wives of Windsor</cite>.</p>

<form method='GET' action='/cgi-bin/likelihood.cgi'>
Analysis ID: <input type='text' name='analysis_id' value='A59527' /><br />
Reference ID: <input type='text' name='reference_id' value='A11988' /><br />
<input type='submit' value='Go' />
</form>

EOF

}


sub template {

	return <<EOF
<html>
<head>
<title>Project English</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="/etc/style.css">
</head>
<body>
<div class="header">
	<h1>Project English - Log-Likelihood ratios</h1>
</div>

<div class="col-3 col-m-3 menu">
  <ul>
    <li><a href="/home.html">Home</a></li>
    <li><a href="/about/">About and scope</a></li>
	<li><a href="/cgi-bin/search.cgi">Search</a></li>
 </ul>
</div>

<div class="col-9 col-m-9">

##CONTENT##

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
	<title>Project English</title>
  	<script type="text/javascript" charset="utf8" src="/etc/jquery-3.0.0.min.js"></script>
	<script type="text/javascript" charset="utf8" src="/etc/DataTables/datatables.js"></script>
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link rel="stylesheet" type="text/css" href="/etc/DataTables/datatables.css">
    <script>
		\$(document).ready(function() {
			\$('#bibliographics').DataTable({"order": [], "paging": false });
		} );
	</script>
</head>
<body>

<h1>##TITLE## - Log-likelihood ratios</h1>

<table id="bibliographics" class="display" cellspacing="0" width="100%">
        <thead>
            <tr>
				<th style='text-align: center'>Word</th>
				<th style='text-align: center'>Relative use</th>
				<th style='text-align: center'>G2</th>
				<th style='text-align: center'>Analysis count</th>
				<th style='text-align: center'>Reference count</th>
				<th style='text-align: center'>Analysis parts/10,000</th>
				<th style='text-align: center'>Reference parts/10,000</th>
            </tr>
        </thead>
        <tfoot>
            <tr>
				<th>Word</th>
				<th>Relative use</th>
				<th>G2</th>
				<th>Analysis count</th>
				<th>Reference count</th>
				<th>Analysis parts/10,000</th>
				<th>Reference parts/10,000</th>
            </tr>
        </tfoot>
		##TBODY##
    </table>
</body>
</html>
EOF
}


