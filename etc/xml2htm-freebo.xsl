<?xml version='1.0'?>
<xsl:stylesheet
	xmlns:xsl='http://www.w3.org/1999/XSL/Transform' 
	xmlns:t="http://www.tei-c.org/ns/1.0"
 	version='1.0' >


	<!-- tei2htm.xsl - create somewhat readable but also intelligent HTML from TEI -->
	<!-- Eric Lease Morgan <emorgan@nd.edu> -->
	<!-- November 1, 2016 - first cut -->
	<!-- November 6, 2016 - getting closer -->
	<!-- June     8, 2017 - added spaces after words and punctuation, dumb! -->

	<xsl:output method='xml' indent='yes' />
  	 		
	<xsl:template match="/t:TEI">
		<html>
		<head>
			<meta charset="utf-8"/>
			<title><xsl:value-of select="t:teiHeader/t:fileDesc/t:titleStmt/t:title" /></title>
		</head>
		<body>
			<h1>
				<xsl:value-of select="t:teiHeader/t:fileDesc/t:titleStmt/t:title" />
				<xsl:text> / </xsl:text>
				<xsl:value-of select="t:teiHeader/t:fileDesc/t:titleStmt/t:author" />
				<xsl:text> (</xsl:text>
				<xsl:value-of select="t:teiHeader/t:fileDesc/t:sourceDesc/t:biblFull/t:publicationStmt" />
				<xsl:text>)</xsl:text>
			</h1>
		<xsl:apply-templates />
		</body>
		</html>
	</xsl:template>				

	<!-- do nothing templates -->
	<xsl:template match="t:teiHeader" />
	<xsl:template match="text()" />

	<!-- heads ought to have... heads -->
	<xsl:template match="t:head">
		<h3><a><xsl:attribute name="name"><xsl:value-of select='./@xml:id' /></xsl:attribute><xsl:apply-templates /></a></h3>
	</xsl:template>				

	<!-- trap "paragraph-like" items -->
	<xsl:template match="t:p|t:sp|t:l|t:opener|t:stage|t:trailer|t:signed">
		<p><a><xsl:attribute name="name"><xsl:value-of select='./@xml:id' /></xsl:attribute><xsl:apply-templates /></a></p>
	</xsl:template>				

	<!-- line groups are special; really? -->
	<xsl:template match="t:lg">
		<p><a><xsl:attribute name="name"><xsl:value-of select='./@xml:id' /></xsl:attribute>
		<xsl:for-each select='./t:l' >
			<xsl:apply-templates /><br />
		</xsl:for-each>
		</a></p>
	</xsl:template>		
	
	<!-- output these -->
	<xsl:template match="t:pc|t:c">
		<xsl:value-of select="." />
		<xsl:text> </xsl:text>
	</xsl:template>	
				
	<!-- output "regularized" version of the given word -->
	<xsl:template match="t:w">
		<xsl:value-of select="./@reg" />
		<xsl:text> </xsl:text>
	</xsl:template>	

</xsl:stylesheet>
