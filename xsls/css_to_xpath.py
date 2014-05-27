#!/usr/bin/env python3
"""Patch cssselect"""

from .tokenizer_exception import UnableToConvertCSSSelector

try:
    from cssselect import GenericTranslator, SelectorError

    class PatchedTranslator(GenericTranslator):
        def __init__(self, offset):
            pass

        def xpath_descendant_combinator(self, left, right):
            """right is a child, grand-child or further descendant of left.
            By default, GenericTranslator converts E F to
            E/descendant-or-self::*/F which is not understood by xslproc
            instead of E//F.
            """
            return left.join('//', right)

except ImportError:
    class PatchedTranslator(object):
        def __init__(self, offset):
            raise UnableToConvertCSSSelector(offset)

