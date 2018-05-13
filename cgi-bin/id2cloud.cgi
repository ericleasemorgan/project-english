#!/usr/bin/perl

use constant TMP   => '../tmp/words.tsv';
use constant CLOUD => '../bin/words2cloud.R';
use constant QUERY => qq( SELECT id, collection FROM titles WHERE id='##ID##'; );
use constant ROOT  => '../';

use strict;
use CGI;
use CGI::Carp qw( fatalsToBrowser );
require '/afs/crc.nd.edu/user/e/emorgan/local/english/lib/english.pl';

my $cgi     = CGI->new;
my $id      = $cgi->param( 'id' );
my $element = $cgi->param( 'element' );

# no input; display home page
if ( ! $id | ! $element ) {

	print $cgi->header;
	print &form;
	
}

else {

	# build a query to search for collections
	my $sql    =  QUERY;
	$sql       =~ s/##ID##/$id/e;
	my $dbh    =  &connect2db;
	my $handle =  $dbh->prepare( $sql );
	$handle->execute() or die $DBI::errstr;
	my $item       = $handle->fetchrow_hashref;
	my $collection = $$item{ 'collection' };
	my $id         = $$item{ 'id' };
	my $file       = ROOT . &id2root( $collection, $id ) . "/$id.ner";

	my %entities = ();
	open INPUT, " < $file" or die "Can't open $file ($!).\n";
	while ( <INPUT> ) {

		chop;
		my ( $id, $type, $entity ) = split( "\t", $_ );
		next if ( $type ne $element );
		$entities{ $entity }++;
	 
	}
	close INPUT;

	my $tmp = TMP;
	open OUTPUT, " > $tmp" or die "Can't open $tmp ($!).\n";
	foreach ( sort { $entities{ $b } <=> $entities{ $a } } keys %entities ) { print OUTPUT join( "\t", ( $_, $entities{ $_ } ) ), "\n" }
	close OUTPUT;

	system( CLOUD );
	print $cgi->redirect( 'http://cds.crc.nd.edu/tmp/cloud.png');

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
	<h1>Project English - Get metadata</h1>
</div>

<div class="col-3 col-m-3 menu">
  <ul>
    <li><a href="/home.html">Home</a></li>
    <li><a href="/about/">About and scope</a></li>
	<li><a href="/cgi-bin/search.cgi">Search</a></li>
 </ul>
</div>

<div class="col-9 col-m-9">

<p>Given an Project English identifier and a type of word, this form will return an word cloud.</p>
<form method='GET' action='/cgi-bin/id2cloud.cgi'>
<input type='text' name='id' size='50' value='A02000'/>
<select name="element">
<option value='PERSON'>people</option>
<option value='ORGANIZATION'>organizations</option>
<option value='LOCATION'>places</option>
</select>

<input type='submit' value='Make word cloud' />
</form>

<div class="footer">

<p style='text-align: right'>
Eric Lease Morgan &amp; Team Project English<br />
April 9, 2018
</p>

</div>

</div>


</body>
</html>
EOF
	
}




