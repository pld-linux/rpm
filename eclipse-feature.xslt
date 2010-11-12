<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text"/>

<!-- we match from root, not to left anything to default template -->
<xsl:template match="/">
	<!-- process provides -->
	<xsl:text>Provides:&#09;eclipse(</xsl:text>
		<xsl:value-of select="//feature/@id"/>
		<xsl:text>) = </xsl:text>
		<xsl:value-of select="//feature/@version"/>
	<xsl:text>&#10;</xsl:text>

	<!-- process requires -->
	<xsl:for-each select="feature/requires/import">
		<xsl:text>Requires:&#09;eclipse(</xsl:text>
			<xsl:value-of select="@plugin"/>
		<xsl:text>)</xsl:text>

		<!-- handle match="perfect" (probably means: same version as us) -->
			<xsl:if test="@match = 'perfect'">
				<xsl:text> = </xsl:text>
				<xsl:value-of select="//feature/@version"/>
			</xsl:if>

		<xsl:text>&#10;</xsl:text>
	</xsl:for-each>
</xsl:template>

</xsl:stylesheet>
