<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text"/>

<!-- we match from root, not to left anything to default template -->
<xsl:template match="/">
	<xsl:apply-templates select="feature"/>
</xsl:template>

<xsl:template match="feature">
	<!-- process provides -->
	<xsl:if test="$mode = 'provides'">
		<!-- include root tag of feature -->
		<xsl:text>eclipse(</xsl:text>
			<xsl:value-of select="@id"/>
			<xsl:text>) = </xsl:text>
			<xsl:value-of select="@version"/>
		<xsl:text>&#10;</xsl:text>

		<!-- is feature and plugin any way different? -->
		<!-- process feature/plugin -->
		<xsl:for-each select="plugin">
			<xsl:text>eclipse(</xsl:text>
				<xsl:value-of select="@id"/>
				<xsl:text>) = </xsl:text>
				<xsl:value-of select="@version"/>
			<xsl:text>&#10;</xsl:text>
		</xsl:for-each>
		<!-- process feature/includes -->
		<xsl:for-each select="includes">
			<xsl:text>eclipse(</xsl:text>
				<xsl:value-of select="@id"/>
				<xsl:text>) = </xsl:text>
				<xsl:value-of select="@version"/>
			<xsl:text>&#10;</xsl:text>
		</xsl:for-each>
	</xsl:if>

	<!-- process requires -->
	<xsl:if test="$mode = 'requires'">
		<xsl:for-each select="requires/import">
			<xsl:text>eclipse(</xsl:text>
				<!-- match plugin or feature -->
				<xsl:if test="@plugin != ''">
					<xsl:value-of select="@plugin"/>
				</xsl:if>
				<xsl:if test="@feature != ''">
					<xsl:value-of select="@feature"/>
				</xsl:if>
			<xsl:text>)</xsl:text>

			<!-- handle match="perfect" (probably means: same version as us) -->
				<xsl:if test="@match = 'perfect'">
					<xsl:text> = </xsl:text>
					<xsl:value-of select="//feature/@version"/>
				</xsl:if>

				<xsl:if test="@match = 'compatible'">
					<xsl:text> >= </xsl:text>
					<xsl:value-of select="@version"/>
				</xsl:if>

				<!-- apparently: base ver or greater -->
				<xsl:if test="@match = 'equivalent'">
					<xsl:text> >= </xsl:text>
					<xsl:value-of select="@version"/>
				</xsl:if>

				<!-- no qualifier, assume any? -->
				<xsl:if test="@match = ''">
					<xsl:text> >= </xsl:text>
					<xsl:value-of select="@version"/>
				</xsl:if>

			<xsl:text>&#10;</xsl:text>
		</xsl:for-each>
	</xsl:if>

</xsl:template>

</xsl:stylesheet>
