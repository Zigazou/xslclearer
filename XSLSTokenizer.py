#!/usr/bin/env python
"""xslsreprocessor compile .xsls files into .xslt files"""

import re

class XSLSTokenizerException(Exception):
    """Exception generated when the Tokenizer is unable to identify a token"""
    pass

class XSLSTokenizer:
    """Tokenizer for .xsls files"""
    def __init__(self):
        # Authorized characters for XML tags taken from
        # http://www.w3.org/TR/xml/
        common_char = ur':A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF'
        common_char += ur'\u0370-\u037D\u037F-\u1FFF\u200C-\u200D'
        common_char += ur'\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF'
        common_char += ur'\uF900-\uFDCF\uFDF0-\uFFFD\U00010000-\U000EFFFF'

        name_start_char = ur'[' + common_char + ur']'
        name_char = ur'[' + common_char
        name_char += ur'.0-9\u00B7\u0300-\u036F\u203F-\u2040-]'

        token_patterns = [ur'(?P<' + name + ur'>' + regexp + ur')'
            for name, regexp in [
                ('identifier', name_start_char + name_char + ur'*'),
                ('string', ur'"(\\"|\\\\|[^"])*"'),
                ('semicolon', ur';'),
                ('comma', ur','),
                ('paropen', ur'[(]'),
                ('parclose', ur'[)]'),
                ('curopen', ur'{'),
                ('curclose', ur'}'),
                ('inplace', ur'\[(\\]|\\\\|[^\]])*\]'),
                ('newline', ur'\n'),
                ('whitespace', ur'\s+'),
                ('equals', ur'='),
                ('comment', ur'//[^\n]*\n')
            ]
        ]

        self.token_re = re.compile(
            ur'|'.join(token_patterns),
            re.VERBOSE | re.UNICODE
        )

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
