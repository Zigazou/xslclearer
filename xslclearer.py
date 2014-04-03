#!/usr/bin/env python
"""xslsreprocessor compile .xsls files into .xslt files"""

import re
import sys

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

class XSLSCompilerException(Exception):
    """Exception generated when the XSLSCompiler encounters a syntax error"""
    pass

class XSLSNoMoreTokenException(Exception):
    """Exception generated when the XSLSCompiler excpected another token
    but there is none available"""
    pass

class XSLSCompiler:
    """The XSLSCompiler reads triplets (token name, value, offset) and produces
    an .xslt file.

    The grammar is very simple :
    program = command*
    command = instruction
            | inplace
    instruction = identifier '(' parameter* ')' '{' program '}'
                | identifier '(' parameter* ')' ';'
    parameter = identifier '=' string
    """
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_pos = 0

    def _syntax_error(self, message):
        """Raise an XSLSCompilerException when there is a syntax error"""
        raise XSLSCompilerException('Compiler stopped at %s(%s, %d): %s' % (
            self.tokens[self.current_pos][0],
            self.tokens[self.current_pos][1],
            self.tokens[self.current_pos][2],
            message
        ))

    def _remaining(self):
        """Returns True if there are still some tokens to compile"""
        return self.current_pos < len(self.tokens)

    def _next_token_is(self, name):
        """Tests if the next available token is of some name"""
        tokname, _, _ = self.tokens[self.current_pos]
        
        if tokname == name:
            return True
        else:
            return False

    def _consume(self, name=None):
        """Consume a token
        If a name is given, the consumed token must have the same name,
        otherwise an exception is generated.
        """
        if not self._remaining():
            raise XSLSNoMoreTokenException('No more token !')

        if name != None and not self._next_token_is(name):
            self._syntax_error('%s' % (name,))

        token = self.tokens[self.current_pos]
        self.current_pos += 1
        return token

    def _read_program(self):
        """Read a program"""
        output = ''
        while self._remaining():
            command = self._read_command()
            
            if command == '':
                break
            
            output += command

        return output

    def _read_command(self):
        """Read a command"""
        if self._next_token_is('identifier'):
            return self._read_instruction()
        elif self._next_token_is('inplace'):
            return self._read_inplace()
        elif self._next_token_is('curclose'):
            return ''
        else:
            self._syntax_error('identifier or inplace expected')

    def _read_inplace(self):
        """Read inplace"""
        _, inplace, _ = self._consume('inplace')
        
        inplace = inplace[1:-1]
        inplace = inplace.replace(r'\]', ']')
        inplace = inplace.replace(r'\\', '\\')
        return inplace

    def _read_instruction(self):
        """Read an instruction"""
        _, instruction, _ = self._consume('identifier')

        params = self._read_parameters()

        if self._next_token_is('semicolon'):
            self._consume('semicolon')
            return '<xsl:%s %s/>' % (instruction, params)
        elif self._next_token_is('curopen'):
            self._consume('curopen')
            
            program = self._read_program()
            
            output = '<xsl:%s %s>%s</xsl:%s>' % (
                instruction, params,
                program,
                instruction
            )
            
            self._consume('curclose')

            return output
        else:
            self._syntax_error('semicolon or curly brace expected')

    def _read_parameters(self):
        """Read a parameter list"""
        self._consume('paropen')

        output = ''
        while self._next_token_is('identifier'):
            output += self._read_parameter()

        self._consume('parclose')

        return output

    def _read_parameter(self):
        """Read a parameter"""
        _, parameter, _ = self._consume('identifier')
        self._consume('equals')
        _, value, _ = self._consume('string')

        value = value.replace("&", "&amp;")
        value = value.replace("<", "&lt;")
        value = value.replace(">", "&gt;")
        value = value.replace(r'\"', "&quot;")
        value = value.replace(r'\\', '\\')

        if self._next_token_is('comma'):
            self._consume('comma')

        return '%s=%s ' % (parameter, value)

    def compile(self):
        """Compile the submitted list of tokens and generate an .xslt file"""
        output = '<?xml version="1.0"?>'
        output += "\n"
        output += self._read_program()
        return output

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
