<?xml version='1.0'?>
<xsl:stylesheet
	xmlns:xsl='http://www.w3.org/1999/XSL/Transform' 
	xmlns:t="http://www.tei-c.org/ns/1.0"
 	version='1.0' >

	<!-- xml2txt-freebo.xsl - create somewhat readable but also intelligent HTML from TEI -->
	<!-- Eric Lease Morgan <emorgan@nd.edu> -->
	<!-- November 1, 2016 - first cut -->
	<!-- November 6, 2016 - getting closer -->
	<!-- June     8, 2017 - added spaces after words and punctuation, dumb! -->

	<xsl:output method="text" encoding="UTF-8" />
	<xsl:strip-space elements="*"/>

	<xsl:template match="/t:TEI">
		<xsl:value-of select="t:teiHeader/t:fileDesc/t:titleStmt/t:title" />
		<xsl:text> / </xsl:text>
		<xsl:value-of select="t:teiHeader/t:fileDesc/t:titleStmt/t:author" />
		<xsl:text> (</xsl:text>
		<xsl:value-of select="t:teiHeader/t:fileDesc/t:sourceDesc/t:biblFull/t:publicationStmt" />
		<xsl:text>)</xsl:text>
		<xsl:text>&#10;&#10;</xsl:text>
		<xsl:apply-templates />
	</xsl:template>				

	<!-- do nothing templates -->
	<xsl:template match="t:teiHeader" />
	<xsl:template match="text()" />

	<!-- heads ought to have... heads -->
	<xsl:template match="t:head">
		<xsl:apply-templates />
	</xsl:template>				

	<!-- trap "paragraph-like" items -->
	<xsl:template match="t:p|t:sp|t:l|t:opener|t:stage|t:trailer|t:signed">
		<xsl:apply-templates />
		<xsl:text>&#10;&#10;</xsl:text>
	</xsl:template>				

	<!-- line groups are special; really? -->
	<xsl:template match="t:lg">
		<xsl:for-each select='./t:l' >
			<xsl:apply-templates /><xsl:text>&#10;</xsl:text>
		</xsl:for-each>
		<xsl:text>&#10;&#10;</xsl:text>
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
