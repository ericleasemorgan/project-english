<?xml version='1.0'?>
<xsl:stylesheet
	xmlns:xsl='http://www.w3.org/1999/XSL/Transform' 
 	version='1.0' >


	<!-- xml2htm-sabin.xsl - create somewhat readable HTML from XML -->
	<!-- Eric Lease Morgan <emorgan@nd.edu> -->
	<!-- April 6, 2018 - first cut -->

	<xsl:output method='xml' indent='yes' />
	<xsl:strip-space elements="*"/>

	<xsl:template match="book">
		<html>
		<head>
			<meta charset="utf-8"/>
			<title><xsl:value-of select="/book/citation/titleGroup/fullTitle"/></title>
		</head>
		<body>
			<h1>
				<xsl:value-of select="/book/citation/titleGroup/fullTitle"/>
				<xsl:text> / </xsl:text>
				<xsl:value-of select="/book/citation/authorGroup/author/marcName"/>
				<xsl:text> (</xsl:text>
				<xsl:value-of select="/book/citation/imprint/imprintFull"/>
				<xsl:text>)</xsl:text>
			</h1>
		<xsl:apply-templates />
		</body>
		</html>
	</xsl:template>				

	<!-- do nothing templates -->
	<xsl:template match="bookInfo"/>
	<xsl:template match="citation"/>
	<xsl:template match="pageInfo"/>

	<!-- trap paragraphs -->
	<xsl:template match="p">
		<p><xsl:apply-templates /></p>
	</xsl:template>

	<!-- output words -->
	<xsl:template match="wd">
		<xsl:value-of select="."/>
		<xsl:text> </xsl:text>
	</xsl:template>

</xsl:stylesheet>
