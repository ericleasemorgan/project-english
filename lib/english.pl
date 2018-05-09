
# configure
use constant DRIVER     => 'SQLite';
use constant DATABASE   => '/afs/crc.nd.edu/user/e/emorgan/local/english/etc/english.db';

# require
use DBI;
use strict;


sub stopwords {

	my $file      = shift;
	my %stopwords = ();
	
	my $stopwords = &slurp( $file );
	foreach my $word ( split( '\n', &slurp( $file ) ) ) { $stopwords{ $word }++ }
	
	return \%stopwords;
		
}


sub escape {

	my $string = shift;

	$string =~ s/&/&amp;/g;
	$string =~ s/</&lt;/g;
	$string =~ s/>/&gt;/g;
	
	return $string;
	
}


sub id2root {

	# configure
	use constant FREEBO => '/collections/freebo';
	use constant ECCO   => '/collections/ecco';
	use constant SABIN  => '/collections/sabin';
	
	# get input
	my $collection = shift;
	my $id         = shift;
	my $results    = '';
	
	if ( $collection eq 'freebo' ) { 
	
		my $prefix  = substr( $id, 0, 3 );
		$results = FREEBO . "/$prefix/$id";
		
	}
	
	if ( $collection eq 'sabin' ) { 
	
		my $prefix  = substr( $id, 3, 3 ) . '/' . substr( $id, 6, 3 );
		$results = SABIN . "/$prefix/$id";
		
	}
	
	if ( $collection eq 'ecco' ) { 
	
		my $prefix  = substr( $id, 0, 2 ) . '/' . substr( $id, 2, 2 );
		$results = ECCO . "/$prefix/$id";
		
	}
	
	# done
	return $results;

}


sub connect2db {

	# get input
	my $driver   = DRIVER;
	my $database = DATABASE;
	
	# do the work
	my $handle = DBI->connect( "DBI:$driver:dbname=$database", '', '', { RaiseError => 1 } ) or die $DBI::errstr;

	# done
	return $handle;
	
}

sub slurp {

	my $f = shift;
	open ( F, $f ) or die "Can't open $f ($!). Call Eric.\n";
	my $r = do { local $/; <F> };
	close F;
	return $r;

}

# return true or die
1;