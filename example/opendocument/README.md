OpenDocument
============

OpenDocument is an example of a OpenDocument manipulation written with
XSLClearer.

Here’s a description of each file.

odt-summary.xsls
----------------

It is an XSLS stylesheet which prints out a summary of an odt file.

To use it :

    unzip -p file.odt content.xml | xslsproc odt-summary.xsls -

odt-styles.xsls
---------------

It is an XSLS stylesheet which prints out the styles associated with an
odt file.

To use it :

    unzip -p file.odt styles.xml | xslsproc odt-styles.xsls -

example/*
---------

The example subdirectory contains the following files:

- le-fer.odt: french text about iron.
- le-fer--content.xml: the XML content file extracted from le-fer.odt
- le-fer--content.xml.png: the tree of the previous file
- le-fer--summary.txt: the output of odt-summary.xsls against
  le-fer--content.xml (list of every title)
- le-fer--styles.xml: the XML styles file extracted from le-fer.odt
- le-fer--styles.xml.png: the tree of the previous file
- le-fer--styles.txt: the output of odt-styles.xsls against le-fer--styles.xml
  (list of every style)

