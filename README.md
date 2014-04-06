XSLClearer
==========

XSLClearer tries to make writing XSL templates easier.

It is a proof of concept. It is therefore in early stage of development.
Though it works on a simple example, it will surely fail at more concrete
case.

It is in fact a very crude compiler (lexical+grammar).

Documentation
-------------

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
