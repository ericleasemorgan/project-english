<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0" >

	<xsl:output method="text" encoding="UTF-8" />
	<xsl:strip-space elements="*"/>

	<!-- outut a citation, and then do the work -->
	<xsl:template match="book">
		<xsl:value-of select="/book/citation/titleGroup/fullTitle"/>
		<xsl:text> / </xsl:text>
		<xsl:value-of select="/book/citation/authorGroup/author/marcName"/>
		<xsl:text> (</xsl:text>
		<xsl:value-of select="/book/citation/imprint/imprintFull"/>
		<xsl:text>)</xsl:text>
		<xsl:text>&#10;&#10;</xsl:text>
		<xsl:apply-templates />
	</xsl:template>

	<!-- do nothing templates -->
	<xsl:template match="bookInfo"/>
	<xsl:template match="citation"/>
	<xsl:template match="pageInfo"/>

	<!-- trap paragraphs -->
	<xsl:template match="p">
		<xsl:apply-templates />
		<xsl:text>&#10;&#10;</xsl:text>
	</xsl:template>

	<!-- output words -->
	<xsl:template match="wd">
		<xsl:value-of select="."/>
		<xsl:text> </xsl:text>
	</xsl:template>

</xsl:stylesheet>