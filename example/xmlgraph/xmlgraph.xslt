<?xml version="1.0"?>
<!-- XML graph -->
<xsl:stylesheet
  version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
>
  <xsl:output method="text" encoding="utf-8" />

  <!-- This parameter can be defined outside of this stylesheet -->
  <xsl:param name="showleaf" select="'false'" />

  <!-- Create a dot node given the parent id, child id, label and shape -->
  <xsl:template name="create-node">
    <xsl:param name="parent" />
    <xsl:param name="child" />
    <xsl:param name="label" />
    <xsl:param name="shape" />

    <!-- Under XSLTProc, generate-id of nothing gives idp0 -->
    <xsl:value-of select="$child" />[label="<xsl:value-of select="$label" />"
    shape=<xsl:value-of select="$shape" />];

    <xsl:if test="$parent != 'idp0'">
      <xsl:value-of select="$parent" /> -&gt; 
      <xsl:value-of select="$child" />;
    </xsl:if>
  </xsl:template>

  <!-- Root of the XML tree -->
  <xsl:template match="/">digraph MyGraph {
    graph [rankdir=LR, splines=polyline, nodesep=0.10];
    <xsl:apply-templates select="@*|node()" />}
  </xsl:template>

  <!-- Each tag will be represented by a text inside a rectangle -->
  <xsl:template match="node()">
    <xsl:variable name="nodelabel">
      <xsl:choose>
        <!-- Show the number of attribute after the tag name -->
        <xsl:when test="count(@*) &gt; 0 and $showleaf = 'false'">
          <xsl:value-of select="concat(name(), ' (',count(@*),')')" />
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="name()" />
        </xsl:otherwise>
      </xsl:choose>
    </xsl:variable>

    <xsl:call-template name="create-node">
      <xsl:with-param name="parent" select="generate-id(..)" />
      <xsl:with-param name="child" select="generate-id(.)" />
      <xsl:with-param name="label" select="$nodelabel" />
      <xsl:with-param name="shape" select="'rect'" />
    </xsl:call-template>

    <xsl:apply-templates select="@*|node()" />
  </xsl:template>

  <!-- Template for attributes -->
  <xsl:template match="@*">
    <xsl:if test="$showleaf = 'true'">
      <xsl:call-template name="create-node">
        <xsl:with-param name="parent" select="generate-id(..)" />
        <xsl:with-param name="child" select="generate-id(.)" />
        <xsl:with-param name="label" select="name()" />
        <xsl:with-param name="shape" select="'oval'" />
      </xsl:call-template>
    </xsl:if>
  </xsl:template>

  <!-- Template for comments -->
  <xsl:template match="comment()">
    <xsl:call-template name="create-node">
      <xsl:with-param name="parent" select="generate-id(..)" />
      <xsl:with-param name="child" select="generate-id(.)" />
      <xsl:with-param name="label" select="'comment'" />
      <xsl:with-param name="shape" select="'plaintext'" />
    </xsl:call-template>
  </xsl:template>

  <!-- Output beginning of texts only if it really contains text -->
  <xsl:template match="text()[normalize-space(.) != '']">
    <xsl:call-template name="create-node">
      <xsl:with-param name="parent" select="generate-id(..)" />
      <xsl:with-param name="child" select="generate-id(.)" />
      <xsl:with-param name="label" select="substring(., 1, 10)" />
      <xsl:with-param name="shape" select="'plaintext'" />
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="text()" />

</xsl:stylesheet>

