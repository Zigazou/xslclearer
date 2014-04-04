#!/usr/bin/env python
"""xslsreprocessor compile .xsls files into .xslt files"""

import re

class XSLSTokenizerException(Exception):
    """Exception generated when the Tokenizer is unable to identify a token"""
    pass

class XSLSTokenizer:
    """Tokenizer for .xsls files"""
    def __init__(self):
        token_patterns = ['(?P<' + name + '>' + regexp + ')'
            for name, regexp in [
                ('identifier', r'[a-zA-Z][a-zA-Z0-9:_-]*'),
                ('string', r'"(\\"|\\\\|[^"])*"'),
                ('semicolon', r';'),
                ('comma', r','),
                ('paropen', r'[(]'),
                ('parclose', r'[)]'),
                ('curopen', r'{'),
                ('curclose', r'}'),
                ('inplace', r'\[(\\]|\\\\|[^\]])*\]'),
                ('newline', r'\n'),
                ('whitespace', r'\s+'),
                ('equals', r'='),
                ('comment', r'//[^\n]*\n')
            ]
        ]

        self.token_re = re.compile('|'.join(token_patterns), re.VERBOSE)

    def tokenize(self, text, skip=None):
        """Tokenizes .xsls files
        
        It yields triplets (token name, value, offset)

        Inspired by:
        http://stackoverflow.com/questions/2358890/
               python-lexical-analysis-and-tokenization
        """

        if skip == None:
            skip = []

        pos = 0
        while True:
            match = self.token_re.match(text, pos)

            if not match:
                break

            pos = match.end()
            tokname = match.lastgroup
            tokvalue = match.group(tokname)

            if not tokname in skip:
                yield tokname, tokvalue, pos

        if pos != len(text):
            raise XSLSTokenizerException(
                'tokenizer stopped at pos %r of %r' % (pos, len(text))
            )
