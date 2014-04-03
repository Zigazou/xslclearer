<?xml version="1.0"?>
<!-- Menus template -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <!-- Output method is XML because if we use HTML, xsltproc will insert
         a meta tag specifying the charset. We do not want it since it is
         not compatible with HTML5 ! -->
    <xsl:output method="xml" omit-xml-declaration="yes" encoding="utf-8" />

    <!-- Absolute image path relatively to the Document Root -->
    <xsl:variable name="imagepath" select="'/path/to/img'" />

    <xsl:variable name="upper" select="'ABCDEFGHIJKLMNOPQRSTUVWXYZ'" />
    <xsl:variable name="lower" select="'abcdefghijklmnopqrstuvwxyz'" />

    <!-- ================================================================= -->
    <!-- Functions                                                         -->
    <!-- ================================================================= -->
    <xsl:template name="day-of-the-week">
        <xsl:param name="num"/>

        <xsl:choose>
            <xsl:when test="$num = 0">Lundi</xsl:when>
            <xsl:when test="$num = 1">Mardi</xsl:when>
            <xsl:when test="$num = 2">Mercredi</xsl:when>
            <xsl:when test="$num = 3">Jeudi</xsl:when>
            <xsl:when test="$num = 4">Vendredi</xsl:when>
            <xsl:when test="$num = 5">Samedi</xsl:when>
            <xsl:when test="$num = 6">Dimanche</xsl:when>
            <xsl:otherwise></xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <!-- ================================================================= -->
    <!-- Apply template to menu tag                                        -->
    <!-- ================================================================= -->
    <xsl:template match="menu">
        <xsl:variable name="firstday" select="@firstday" />

        <xsl:for-each select="day">
            <!-- Ignore days with no meal -->
            <xsl:if test="string-length(main) &gt; 0">
                <h2>
                    <xsl:call-template name="day-of-the-week">
                        <xsl:with-param name="num" select="@num"/>
                    </xsl:call-template>
                </h2>
                <ul>
                    <xsl:apply-templates/>
                </ul>
            </xsl:if>
        </xsl:for-each>
    </xsl:template>

    <!-- ================================================================= -->
    <!-- Templates for dishes                                              -->
    <!-- ================================================================= -->
    <xsl:template match="extra|starter|main|vegetable|dairy|dessert">
        <xsl:if test="string-length(.) &gt; 0">
            <li class="{local-name()}"><xsl:apply-templates/></li>
        </xsl:if>
    </xsl:template>

    <!-- Snacks are a little bit different -->
    <xsl:template match="snack">
        <xsl:if test="string-length(.) &gt; 0">
            <li class="{local-name()}">Goûter&#160;: <xsl:apply-templates/></li>
        </xsl:if>
    </xsl:template>

    <!-- ================================================================= -->
    <!-- Templates for labels/pictograms                                   -->
    <!-- ================================================================= -->
    <xsl:template match="label">
        <xsl:param name="id" select="translate(@name, $upper, $lower)" />
        <xsl:param name="title">
            <xsl:choose>
                <xsl:when test="@name = 'AB'">Agriculture biologique</xsl:when>
                <xsl:when test="@name = 'HN'">Produit de Haute-Normandie</xsl:when>
                <xsl:when test="@name = 'BN'">Produit de Basse-Normandie</xsl:when>
                <xsl:when test="@name = 'O3'">Oméga 3 naturels</xsl:when>
                <xsl:when test="@name = 'VPF'">Viande de porc française</xsl:when>
                <xsl:when test="@name = 'VBF'">Viande bovine française</xsl:when>
                <xsl:when test="@name = 'VF'">Volaille française</xsl:when>
                <xsl:otherwise></xsl:otherwise>
            </xsl:choose>
        </xsl:param>

        <span class="picto-title" title="{$title}">
            <img class="picto-rest picto-rest-{$id}"
                 src="{$imagepath}/rest-{$id}.png"
                 title="{$title}"
            />
        </span>
    </xsl:template>
</xsl:stylesheet>
