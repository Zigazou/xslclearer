XSLClearer
==========

XSLClearer tries to make writing XSL templates easier.

It is a proof of concept. It is therefore in early stage of development.
Though it works on a simple example, it will surely fail at more concrete
case.

It is in fact a very crude compiler (lexical+grammar).

Documentation
-------------

### Tags ###

The xsls format converts :

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

If you need to use a closing bracket inside the [ ], you may escape it using
the back-slash.

If you need to use a double quote inside the " ", you may escape it using
the back-slash.

### Variables ###

The xsls format converts :

    $variable = "string";

into

    <xsl:variable name="variable" select="string" />
    
The xsls format converts :

    $variable = {
        instructions
    }

into

    <xsl:variable name="variable">
        instructions
    </xsl:variable>

### Tags with only one attribute ###

The xsls format converts :

    call-template("string") {
        instructions
    }

into

    <xsl:call-template name="string">
        instructions
    </xsl:call-template>

It works for the following tags (attribute) :

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

### Tag and attribute verification ###

The compiler verifies that identifiers are from the XSL or XSL-FO tags lists.
Specifying a namespace disables the verification.

The verification alsa applies to the attributes.

Install
-------

Just place the xslclearer.py in a directory pointed to by the PATH variable
environment, make it executable and that’s all !

If you want syntax highlighting in gedit, you can copy the xsls.lang file to
the /usr/share/gtksourceview-3.0/language-specs directory (adjust it
accordingly to your configuration).

Requirements
------------

XSLClearer has been developped with Python 3.

It only requires the re and sys modules.

Usage
-----

    python xslclearer.py input.xsls > output.xslt
    
    cat input.xsls | python xslclearer.py > output.xslt

Example
-------

The example directory contains an example of an XSL template converted to XSLS
and a file called menu.xml on which the template works. 
