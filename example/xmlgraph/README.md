XMLGraph
========

XMLGraph is an example of a small application based on XSLClearer.

Here’s a description of each file.

xmlgraph
--------

It is a Bash script which creates a PNG file displaying the tree of an XML
file.

For more information on how to use it, just run xmlgraph -h

xmlgraph.xsls
-------------

It is an XSLS stylesheet which transforms an XML file into a dot file.

xmlgraph.xslt
-------------

It is an XSLT version of xmlgraph.xsls which exists only as a comparison
between XSLS and XSLT stylesheets.

example/*
---------

The example subdirectory contains SVG files which comes from the Open Clip Art
Library (http://www.openclipart.org/) :

- emblem-favorite.svg - Gnome - GPLv2
- pictograms-hazard_signs-35.svg - Public domain

Along with them is their XML trees generated by XMLGraph in PNG format.

