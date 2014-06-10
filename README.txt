==========
XSLClearer
==========

XSLClearer tries to make writing XSL templates easier.

It is a proof of concept. It is therefore in early stage of development.
Though it works on a simple example, it will surely fail at more concrete
case.

It is in fact a very crude compiler (lexical+grammar).

Documentation
=============

Tags
----

The xsls format converts:

    tag(attribute="value", attribute="value") {
        tag(attribute="value", attribute="value");
        tag();

        tag(attribute="value") {
            [<tag>Hello</tag>]
        }
    }

into

    <xsl:tag attribute="value" attribute="value">
        <xsl:tag attribute="value" attribute="value" />
        <xsl:tag />
        
        <xsl:tag attribute="value">
            <tag>Hello</tag>
        </xsl:tag>
    </xsl:tag>

XSLClearer recognizes tags and attributes up to XSLT 3.0. A tag/attribute
without a preceding namespace must be and XSLT 3.0 or XSLT-FO tag/attribute.
It otherwise throw an error. If there is a preceding namespace, no check is
done.

If you need to use a closing bracket inside the [ ], you may escape it using
the back-slash.

If you need to use a double quote inside the " ", you may escape it using
the back-slash.

Variables
---------

The xsls format converts:

    $variable = "string";

into

    <xsl:variable name="variable" select="string" />
    
The xsls format converts:

    $variable = {
        instructions
    }

into

    <xsl:variable name="variable">
        instructions
    </xsl:variable>

Strings
-------

Strings are enclosed with double quotes ("). It accepts \ as an escaping
character (\\ to insert \, \" to insert " inside a string).

Special XML characters are automatically escaped.

Example:

    "string-length(\"abc\") > 2"

translates into:

    "string-length(&quot;abc&quot;) &gt; 2"

CSS selector strings
--------------------

Strings can contain CSS selector if they are directly preceded by a #.

Example:

    #"ns|tag ns|tag#identifier"

translates into:

    "//ns:tag//ns:tag[@id='identifier']"

It uses the **cssselect** Python module to do the conversion.

If this module is missing, xslclearer raises an exception.

Tags with only one attribute
----------------------------

The xsls format converts:

    call-template("string") {
        instructions
    }

into

    <xsl:call-template name="string">
        instructions
    </xsl:call-template>

It works for the following tags (attribute):

* when (test),
* if (test),
* for-each (select),
* call-template (name),
* include (href),
* import (href),
* copy (use-attribute-sets),
* copy-of (select),
* message (terminate),
* preserve-space (elements),
* strip-space (elements),
* text (disable-output-escaping).

Though they may have more than one attribute, it also works for the following
tags (attribute):

* value-of (select),
* apply-templates (select),
* template (name),
* attribute (name).

In this case, the argument must be given at the very first position.

Example:

    template("template-name", match="*") {
        ...
    }

translates into:

    <xsl:template name="template-name" match="*">
        ...
    </xsl:template>

Tag and attribute verification
------------------------------

The compiler verifies that identifiers are from the XSL or XSL-FO tags lists.
Specifying a namespace disables the verification.

The verification alsa applies to the attributes.

Install
=======

Just place the xslclearer.py in a directory pointed to by the PATH variable
environment, make it executable and that’s all !

If you want syntax highlighting in gedit, you can copy the xsls.lang file to
the /usr/share/gtksourceview-3.0/language-specs directory (adjust it
accordingly to your configuration).

Requirements
============

XSLClearer has been developped with Python 3.

It only requires the re and sys modules.

Usage
=====

    python3 xslclearer.py input.xsls > output.xslt
    
    cat input.xsls | python3 xslclearer.py > output.xslt

    xslsproc style.xsls input.xml > output

The xslsproc is a wrapper for the xsltproc command. It analyzes the options to
find the an xsls file. If it can be found, the file is transparently converted
to an xslt stylesheet and feed to xsltproc. Every other option is passed
without any change. You can therefore use xslsproc exactly like you would use
xsltproc except it understands xsls files and not xslt files.

Example
=======

The example directory contains an example of an XSL template converted to XSLS
and a file called menu.xml on which the template works. 
