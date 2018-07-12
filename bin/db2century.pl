#!/afs/crc.nd.edu/user/e/emorgan/bin/perl

# db2century.pl - given a century (14, 15, 16, etc.), output paths to text files

# Eric Lease Morgan <emorgan@nd.edu>
# June 21, 2018 - first investigations


# configure
use constant QUERY => 'select id, collection from titles where century is ?';
use constant ROOT  => '.';

# require
use DBI;
use strict;
require '/afs/crc.nd.edu/user/e/emorgan/local/english/lib/english.pl';

my $century = $ARGV[ 0 ];
if ( ! $century ) { die "Usage: $0 <15|16|17|18|19|20>\n" }

# query the database
my $english = &connect2db;
my $handle  = $english->prepare( QUERY );
$handle->execute( $century ) or die $DBI::errstr;

# process each found row
while ( my $row = $handle->fetchrow_hashref ) {

	my $id         = $$row{ 'id' };
	my $collection = $$row{ 'collection' };

	print( ROOT . &id2root( $collection, $id ) . "/$id.txt\n" );

}

# done
exit;
