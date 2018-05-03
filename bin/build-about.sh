#!/usr/bin/env bash

# configure
HOME='/afs/crc.nd.edu/user/e/emorgan/local/english'
ABOUT='./about'
DB='./etc/english.db'
CATALOG="./about/catalog.tsv"
COLLECTIONS='./about/collections.tsv'
FREEBO="./about/freebo.tsv"
ECCO="./about/ecco.tsv"
SABIN="./about/sabin.tsv"
LANGUAGES='./about/languages.tsv'
CITIES='./about/cities.tsv'
CENTURIES='./about/centuries.tsv'
INDEX='index.html'

# make sane
cd $HOME
mkdir -p $ABOUT

# total number of items
TOTALCOLLECTIONITEMS=$( echo "SELECT (COUNT(id)/1000) FROM TITLES WHERE TITLE LIKE '%';" | sqlite3 $DB )

# total number of pages
TOTALCOLLECIONPAGES=$( echo "SELECT (SUM(pages)/1000) FROM TITLES WHERE TITLE LIKE '%';" | sqlite3 $DB )

# average number of pages
AVGERAGECOLLECIONPAGES=$( echo "SELECT CAST(ROUND(AVG(pages)) AS INT) FROM TITLES WHERE TITLE LIKE '%';" | sqlite3 $DB )

# total number of pages
TOTALCOLLECTIONWORDS=$( echo "SELECT (SUM(words)/1000000000) FROM TITLES WHERE TITLE LIKE '%';" | sqlite3 $DB )

# total number of pages
AVERAGECOLLECTIONWORDS=$( echo "SELECT CAST(ROUND(AVG(words)) AS INT) FROM TITLES WHERE TITLE LIKE '%';" | sqlite3 $DB )

# languages
COUNTCOLLECTIONLANGUAGES=$(echo "SELECT COUNT(DISTINCT(language)) FROM titles;" | sqlite3 $DB )

# cities
COUNTCOLLECTIONCITIES=$(echo "SELECT COUNT(DISTINCT(city)) FROM titles;" | sqlite3 $DB )

# get the catalog data and save it
(sqlite3 $DB <<EOF
.mode tabs
.headers on
SELECT year, pages, words FROM titles WHERE title like '%';
EOF
) > $CATALOG

# get collection data
(sqlite3 $DB <<EOF
.mode tabs
.headers on
SELECT count(collection) AS c, collection FROM titles GROUP BY collection ORDER BY c DESC;
EOF
) > $COLLECTIONS

# get collection data
(sqlite3 $DB <<EOF
.mode tabs
.headers on
SELECT count(city) AS c, city FROM titles GROUP BY city ORDER BY c DESC;
EOF
) > $CITIES

# get collection data
(sqlite3 $DB <<EOF
.mode tabs
.headers on
SELECT count(language) AS c, language FROM titles GROUP BY language ORDER BY c DESC;
EOF
) > $LANGUAGES

# centuries
(sqlite3 $DB <<EOF
.mode tabs
.headers on
SELECT count(century) AS c, century FROM titles GROUP BY century ORDER BY c DESC;
EOF
) > $CENTURIES

# get & save freebo
(sqlite3 $DB <<EOF
.mode tabs
.headers on
SELECT year, pages, words FROM titles WHERE title like '%' AND collection='freebo';
EOF
) > $FREEBO

# get & save ecco
(sqlite3 $DB <<EOF
.mode tabs
.headers on
SELECT year, pages, words FROM titles WHERE title like '%' AND collection='ecco';
EOF
) > $ECCO

# get & save sabin
(sqlite3 $DB <<EOF
.mode tabs
.headers on
SELECT year, pages, words FROM titles WHERE title like '%' AND collection='sabin';
EOF
) > $SABIN

# create graphs
cd $ABOUT
../bin/graph-catalog.R

# build the html
HTML="<html>

<head>
<title>Project English - About and scope</title>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<link rel='stylesheet' href='/etc/style.css'>
</head>

<body>

<div class='header'>
	<h1>Project English - About and scope</h1>
</div>

<div class='col-3 col-m-3 menu'>
  <ul>
    <li><a href='/home.html'>Home</a></li>
    <li><a href='/about/'>About and scope</a></li>
    <li><a href='/cgi-bin/search.cgi'>Search</a></li>
  </ul>
</div>

<div class='col-9 col-m-9'>
<p>This page outlines and illustrates the content of Project English as well as each of its 3 sub-collections.</p>

<h2>The whole collection</h2>

<p>The whole collection is currently made up of approximately $TOTALCOLLECTIONITEMS thousand items, $TOTALCOLLECIONPAGES thousand pages, and $TOTALCOLLECTIONWORDS billion words. Which means, on average, each item is about $AVGERAGECOLLECIONPAGES pages (or $AVERAGECOLLECTIONWORDS words) long. There are $COUNTCOLLECTIONLANGUAGES distinct languages represented in the collection, but for all intents &amp; purposes, English is the only language. Similarly, there are $COUNTCOLLECTIONCITIES distinct cities of publication, but about 75% of them are either London, Boston, Dublin, Edinburgh, New York, or Philadelphia.</p>

<table>
<tr><td><img width='400' src='/about/catalog-histogram-pages.png' /></td><td><img width='400' src='/about/catalog-boxplot-pages.png' /></td></tr>
<tr><td><img width='400' src='/about/catalog-histogram-words.png' /></td><td><img width='400' src='/about/catalog-boxplot-words.png' /></td></tr>
<tr><td><img width='400' src='/about/catalog-histogram-years.png' /></td><td><img width='400' src='/about/catalog-boxplot-years.png' /></td></tr>
<tr><td><img width='400' src='/about/catalog-pie-collections.png' /></td><td><img width='400' src='/about/catalog-pie-centuries.png' /></td></tr>
<tr><td><img width='400' src='/about/catalog-pie-languages.png' /></td><td><img width='400' src='/about/catalog-pie-cities.png' /></td></tr>
</table>

<h2>Freebo</h2>
<table>
<tr><td><img width='400' src='/about/freebo-histogram-years.png' /></td><td><img width='400' src='/about/freebo-boxplot-years.png' /></td></tr>
<tr><td><img width='400' src='/about/freebo-histogram-pages.png' /></td><td><img width='400' src='/about/freebo-boxplot-pages.png' /></td></tr>
<tr><td><img width='400' src='/about/freebo-histogram-words.png' /></td><td><img width='400' src='/about/freebo-boxplot-words.png' /></td></tr>
</table>

<h2>ECCO</h2>
<table>
<tr><td><img width='400' src='/about/ecco-histogram-years.png' /></td><td><img width='400' src='/about/ecco-boxplot-years.png' /></td></tr>
<tr><td><img width='400' src='/about/ecco-histogram-pages.png' /></td><td><img width='400' src='/about/ecco-boxplot-pages.png' /></td></tr>
<tr><td><img width='400' src='/about/ecco-histogram-words.png' /></td><td><img width='400' src='/about/ecco-boxplot-words.png' /></td></tr>
</table>


<h2>Sabin</h2>
<table>
<tr><td><img width='400' src='/about/sabin-histogram-years.png' /></td><td><img width='400' src='/about/sabin-boxplot-years.png' /></td></tr>
<tr><td><img width='400' src='/about/sabin-histogram-pages.png' /></td><td><img width='400' src='/about/sabin-boxplot-pages.png' /></td></tr>
<tr><td><img width='400' src='/about/sabin-histogram-words.png' /></td><td><img width='400' src='/about/sabin-boxplot-words.png' /></td></tr>
</table>
	
	
	<div class='footer'>
		<p style='text-align: right'>
		Eric Lease Morgan &amp; Team Project English<br />
		April 6, 2018
		</p>
	</div>

</div>

</body>
</html>"
echo $HTML > $INDEX

# done
exit
