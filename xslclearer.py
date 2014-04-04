#!/usr/bin/env python
"""xslclearer compile .xsls files into .xslt files"""

import sys
from XSLSTokenizer import XSLSTokenizer
from XSLSCompiler import XSLSCompiler

def offset_to_column_line(text, offset):
    if offset > len(text):
        return False

    lines = '\n'.split(text)

    for line_number in xrange(0, len(lines)):
        line_length = len(lines[line_number])

        if offset < line_length:
            break

        offset -= line_length

    return (line_number, offset)

def xsls_compile(xsls_file):
    """Converts an .xsls file into an .xslt file"""
    xslstext = xsls_file.read()

    tokenizer = XSLSTokenizer()

    skips = ['whitespace', 'comment', 'newline']
    tokens = [token for token in tokenizer.tokenize(xslstext, skips)]

    try:
        compiler = XSLSCompiler(tokens)
        return compiler.compile()
    except XSLSCompilerException as e:
        row, column = offset_to_column_line
        return "%s at row %d, column %d" % (e.message, row, column)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(xsls_compile(sys.stdin))
    else:
        print(xsls_compile(open(sys.argv[1])))
