#!/usr/bin/env Rscript

# graph-catalog.R - given the name of a collection, literally illustrate characteristics of the catalog

# Eric Lease Morgan <emorgan@nd.edu>
# June 3, 2015 - first investigations


# configure
CATALOG     = './catalog.tsv'
FREEBO      = './freebo.tsv'
ECCO        = './ecco.tsv'
SABIN       = './sabin.tsv'
COLLECTIONS = './collections.tsv'
CENTURIES   = './centuries.tsv'
LANGUAGES   = './languages.tsv'
CITIES     = './cities.tsv'

# read and parse catalog
catalog =  read.table( CATALOG, sep='\t', header=T, quote = '' )
years   <- catalog$year
pages   <- catalog$pages
words   <- catalog$words

# create boxplots and histograms for each of the numeric columns; dates
png( filename = ( 'catalog-boxplot-years.png' ) )
boxplot( years, main="Years", outline=FALSE )
png( filename = ( 'catalog-histogram-years.png' ) )
hist( years, freq=FALSE, main="Years")
curve( dnorm( x, mean=mean( years ), sd=sd( years ) ), add=TRUE, col="darkblue", lwd=2 )

# pages
png( filename = ( 'catalog-boxplot-pages.png' ) )
boxplot( pages, main="Pages", outline=FALSE )
png( filename = ( 'catalog-histogram-pages.png' ) )
hist( log(pages), freq=FALSE, main="Pages")
#curve( dnorm( x, mean=mean( pages ), sd=sd( pages ) ), add=TRUE, col="darkblue", lwd=2 )

# words
png( filename = ( 'catalog-boxplot-words.png' ) )
boxplot( words, main="Words", outline=FALSE )
png( filename = ( 'catalog-histogram-words.png' ) )
hist( log(words), freq=FALSE, main="Words")
#curve( dnorm( x, mean=mean( words ), sd=sd( words ) ), add=TRUE, col="darkblue", lwd=2 )

# read and parse catalog
catalog =  read.table( COLLECTIONS, sep='\t', header=T, quote = '' )
slices   <- catalog$c
labels   <- catalog$collection
png( filename = ( 'catalog-pie-collections.png' ) )
pie(slices, labels = labels, main="Sub-collections")

# read and parse catalog
catalog =  read.table( CENTURIES, sep='\t', header=T, quote = '' )
slices   <- catalog$c
labels   <- catalog$century
png( filename = ( 'catalog-pie-centuries.png' ) )
pie(slices, labels = labels, main="Centuries")

# collection languages
catalog =  read.table( LANGUAGES, sep='\t', header=T, quote = '' )
slices   <- catalog$c
labels   <- catalog$language
png( filename = ( 'catalog-pie-languages.png' ) )
pie(slices, labels = labels, main="Languages")

# collection cities
catalog =  read.table( CITIES, sep='\t', header=T, quote = '' )
slices   <- catalog$c
labels   <- catalog$city
png( filename = ( 'catalog-pie-cities.png' ) )
pie(slices, labels = labels, main="Cities of publication")

# freebo
catalog =  read.table( FREEBO, sep='\t', header=T, quote = '' )
years   <- catalog$year
pages   <- catalog$pages
words   <- catalog$words

# create boxplots and histograms for each of the numeric columns; dates
png( filename = ( 'freebo-boxplot-years.png' ) )
boxplot( years, main="Years", outline=FALSE )
png( filename = ( 'freebo-histogram-years.png' ) )
hist( years, freq=FALSE, main="Years")
curve( dnorm( x, mean=mean( years ), sd=sd( years ) ), add=TRUE, col="darkblue", lwd=2 )

# pages
png( filename = ( 'freebo-boxplot-pages.png' ) )
boxplot( pages, main="Pages", outline=FALSE )
png( filename = ( 'freebo-histogram-pages.png' ) )
hist( log(pages), freq=FALSE, main="Pages")
#curve( dnorm( x, mean=mean( pages ), sd=sd( pages ) ), add=TRUE, col="darkblue", lwd=2 )

# words
png( filename = ( 'freebo-boxplot-words.png' ) )
boxplot( words, main="Words", outline=FALSE )
png( filename = ( 'freebo-histogram-words.png' ) )
hist( log(words), freq=FALSE, main="Words")
#curve( dnorm( x, mean=mean( words ), sd=sd( words ) ), add=TRUE, col="darkblue", lwd=2 )


# ecco
catalog =  read.table( ECCO, sep='\t', header=T, quote = '' )
years   <- catalog$year
pages   <- catalog$pages
words   <- catalog$words

# create boxplots and histograms for each of the numeric columns; dates
png( filename = ( 'ecco-boxplot-years.png' ) )
boxplot( years, main="Years", outline=FALSE )
png( filename = ( 'ecco-histogram-years.png' ) )
hist( years, freq=FALSE, main="Years")
curve( dnorm( x, mean=mean( years ), sd=sd( years ) ), add=TRUE, col="darkblue", lwd=2 )

# pages
png( filename = ( 'ecco-boxplot-pages.png' ) )
boxplot( pages, main="Pages", outline=FALSE )
png( filename = ( 'ecco-histogram-pages.png' ) )
hist( log(pages), freq=FALSE, main="Pages")
#curve( dnorm( x, mean=mean( pages ), sd=sd( pages ) ), add=TRUE, col="darkblue", lwd=2 )

# words
png( filename = ( 'ecco-boxplot-words.png' ) )
boxplot( words, main="Words", outline=FALSE )
png( filename = ( 'ecco-histogram-words.png' ) )
hist( log(words), freq=FALSE, main="Words")
#curve( dnorm( x, mean=mean( words ), sd=sd( words ) ), add=TRUE, col="darkblue", lwd=2 )


# sabin
catalog =  read.table( SABIN, sep='\t', header=T, quote = '' )
years   <- catalog$year
pages   <- catalog$pages
words   <- catalog$words

# create boxplots and histograms for each of the numeric columns; dates
png( filename = ( 'sabin-boxplot-years.png' ) )
boxplot( years, main="Years", outline=FALSE )
png( filename = ( 'sabin-histogram-years.png' ) )
hist( years, freq=FALSE, main="Years")
curve( dnorm( x, mean=mean( years ), sd=sd( years ) ), add=TRUE, col="darkblue", lwd=2 )

# pages
png( filename = ( 'sabin-boxplot-pages.png' ) )
boxplot( pages, main="Pages", outline=FALSE )
png( filename = ( 'sabin-histogram-pages.png' ) )
hist( log(pages), freq=FALSE, main="Pages")
#curve( dnorm( x, mean=mean( pages ), sd=sd( pages ) ), add=TRUE, col="darkblue", lwd=2 )

# words
png( filename = ( 'sabin-boxplot-words.png' ) )
boxplot( words, main="Words", outline=FALSE )
png( filename = ( 'sabin-histogram-words.png' ) )
hist( log(words), freq=FALSE, main="Words")
#curve( dnorm( x, mean=mean( words ), sd=sd( words ) ), add=TRUE, col="darkblue", lwd=2 )


