#!/usr/bin/env python3
import unittest
import xsls

def suite():
    suite = unittest.TestSuite()
    suite.addTests(TestTokenizer(input, output) for input, output in
        [
            ("abcdef aaa", ('identifier', 'abcdef', 6)),
            ("$abcdef aaa", ('variable', '$abcdef', 7)),
            ('"abcdef"aaa', ('string', '"abcdef"', 8)),
            (";aaa", ('semicolon', ';', 1)),
            ("(aaa", ('paropen', '(', 1)),
            (")aaa", ('parclose', ')', 1)),
            ("{aaa", ('curopen', '{', 1)),
            ("}aaa", ('curclose', '}', 1)),
            ("[akjei]aaa", ('inplace', '[akjei]', 7)),
            ('   ', ('whitespace', '   ', 3)),
            ("\r\n", ('newline', "\r\n", 2)),
            ("=aaa", ('equals', '=', 1)),
            ('// abcdef\naa', ('comment', '// abcdef\n', 10)),
            ('"abc\\""aaa', ('string', '"abc\\""', 7)),
            ('"abc\\\\"aa', ('string', '"abc\\\\"', 7)),
            ('[aaa\\]]aaa', ('inplace', '[aaa\\]]', 7)),
            ('[aaa\\\\]aaa', ('inplace', '[aaa\\\\]', 7)),
        ]    
    )
    return suite

class TestTokenizer(unittest.TestCase):
    def __init__(self, input, output):
        super(TestTokenizer, self).__init__()
        self.input = input
        self.output = output
 
    def runTest(self):
        tokenizer = xsls.Tokenizer()
        self.assertEqual(next(tokenizer.tokenize(self.input)), self.output)
 
if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
