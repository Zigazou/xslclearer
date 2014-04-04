#!/usr/bin/env python
"""xslclearer compile .xsls files into .xslt files"""

import sys
from XSLSTokenizer import XSLSTokenizer
from XSLSCompiler import XSLSCompiler

def xsls_compile(xsls_file):
    """Converts an .xsls file into an .xslt file"""
    xslstext = xsls_file.read()

    tokenizer = XSLSTokenizer()

    skips = ['whitespace', 'comment', 'newline']
    tokens = [token for token in tokenizer.tokenize(xslstext, skips)]

    compiler = XSLSCompiler(tokens)
    
    return compiler.compile()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(xsls_compile(sys.stdin))
    else:
        print(xsls_compile(open(sys.argv[1])))
