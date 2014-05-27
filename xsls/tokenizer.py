#!/usr/bin/env python3
"""XSLSTokenizer is the lexical analyzer of xslclearer."""

from .tokenizer_exception import (
    UnexpectedCharacter,
    InvalidSelector,
    UnableToConvertCSSSelector
)

import re
from .css_to_xpath import PatchedTranslator

class Tokenizer:
    """Tokenizer for .xsls files"""
    def __init__(self):
        # Authorized characters for XML tags taken from
        # http://www.w3.org/TR/xml/
        common_char = (
            ':A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D'
            '\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF'
            '\uF900-\uFDCF\uFDF0-\uFFFD\U00010000-\U000EFFFF'
        )

        name_start_char = '[{common}]'.format(common=common_char)
        name_char = '[{common}{extra}]'.format(
            common=common_char,
            extra='.0-9\u00B7\u0300-\u036F\u203F-\u2040-'
        )

        token_patterns = ['(?P<' + name + '>' + regexp + ')'
            for name, regexp in [
                ('identifier', name_start_char + name_char + '*'),
                ('variable', '\\$' + name_start_char + name_char + '*'),
                ('string', '[#]?"(\\\\"|\\\\\\\\|[^"])*"'),
                ('semicolon', ';'),
                ('comma', ','),
                ('paropen', '[(]'),
                ('parclose', '[)]'),
                ('curopen', '{'),
                ('curclose', '}'),
                ('inplace', '[#]?\\[(\\\\]|\\\\\\\\|[^\\]])*\\]'),
                ('newline', '\\r\\n|\\n|\\r'),
                ('whitespace', '\\s+'),
                ('equals', '='),
                ('comment', '//[^\\n]*\\n')
            ]
        ]

        self.token_re = re.compile(
            '|'.join(token_patterns),
            re.VERBOSE | re.UNICODE
        )

    def _preprocess(self, token_name, token_value, position):
        if token_name == 'string':
            # Unescapes string
            token_value = token_value.replace('\\\\', '\\')
            token_value = token_value.replace('\\"', '"')
            
            if token_value[0] == '#':
                token_value = token_value[2:-1]

                token_value = PatchedTranslator(position).css_to_xpath(
                    token_value,
                    prefix='//'
                )
                    
            else:
                token_value = token_value[1:-1]
        elif token_name == 'variable':
            # Remove the preceding $
            token_value = token_value[1:]
        elif token_name == 'inplace':
            token_value = token_value.replace(r'\]', ']')
            token_value = token_value.replace(r'\\', '\\')

            if token_value[0] == '#':
                token_value = token_value[2:-1]
                token_value = '{start}{value}{end}'.format(
                    start='<text xml:space="preserve">',
                    value=token_value,
                    end='</text>'
                )
            else:
                token_value = token_value[1:-1]

        return token_value
  

    def tokenize(self, text, skip=None):
        """Tokenizes .xsls files
        
        It yields triplets (token name, value, offset) if the token name is
        not included in the skip list.

        Inspired by:
        http://stackoverflow.com/questions/2358890/
               python-lexical-analysis-and-tokenization
        """

        if skip == None:
            skip = []

        position = 0
        while True:
            match = self.token_re.match(text, position)

            if not match:
                break

            position = match.end()
            token_name = match.lastgroup
            token_value = self._preprocess(
                token_name,
                match.group(token_name),
                position
            )

            if not token_name in skip:
                yield token_name, token_value, position

        if position != len(text):
            raise UnexpectedCharacter(position)
