#!/usr/bin/env python3
"""Compiler compiles tokens discovered by Tokenizer into .xslt files"""

from .CompilerException import (
    UnexpectedToken,
    UnknownIdentifier, 
    UnknownAttribute,
    AmbiguousIdentifier,
    NoMoreTokenException
)

from .keywords.xslt_attributes import XSLT_ATTRIBUTES
from .keywords.xslt_tags import XSLT_TAGS
from .keywords.xsl_fo_attributes import XSL_FO_ATTRIBUTES
from .keywords.xsl_fo_tags import XSL_FO_TAGS

XSL_ALL_TAGS = XSLT_TAGS + XSL_FO_TAGS
XSL_ALL_ATTRIBUTES = XSLT_ATTRIBUTES + XSL_FO_ATTRIBUTES

def multiple_replace(text, replaces):
    for origin, destination in replaces:
        text = text.replace(origin, destination)

    return text

class Compiler:
    """The Compiler reads triplets (token name, value, offset) and produces
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

    def _remaining(self):
        """Returns True if there are still some tokens to compile"""
        return self.current_pos < len(self.tokens)

    def _next_token(self):
        """Returns the next token"""
        return self.tokens[self.current_pos]

    def _next_offset(self):
        """Returns current offset in the source file"""
        return self.tokens[self.current_pos][2]

    def _next_token_is(self, name):
        """Tests if the next available token is of some name"""
        token_name, _, _ = self._next_token()
        
        return token_name == name

    def _consume(self, name=None):
        """Consume a token
        If a name is given, the consumed token must have the same name,
        otherwise an exception is generated.
        """
        if not self._remaining():
            raise NoMoreTokenException('No more token !')

        if name != None and not self._next_token_is(name):
            raise UnexpectedToken(
                self._next_offset(),
                self._next_token(),
                name                
            )

        self.current_pos += 1
        return self.tokens[self.current_pos - 1]

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
            raise UnexpectedToken(
                self._next_offset(),
                self._next_token(),
                'identifier or inplace'
            )

    def _read_inplace(self):
        """Read inplace"""
        _, inplace, _ = self._consume('inplace')
        
        return multiple_replace(inplace[1:-1], (
            (r'\]', ']'),
            (r'\\', '\\')
        ))

    def _read_instruction(self):
        """Read an instruction"""
        _, instruction, _ = self._consume('identifier')

        if ':' not in instruction and instruction not in XSL_ALL_TAGS:
            raise UnknownIdentifier(self._next_offset(), instruction)

        params = self._read_parameters()

        # Guess the namespace for the given instruction
        if ':' in instruction:
            namespace = instruction.split(':')[0]
            instruction = instruction.split(':')[1]
        else:
            if instruction in XSLT_TAGS and instruction in XSL_FO_TAGS:
                raise AmbiguousIdentifier(
                    self._next_offset(),
                    instruction
                )

            if instruction in XSLT_TAGS:
                namespace = 'xsl'
            else:
                namespace = 'fo'

        # Generate the XML tags
        if self._next_token_is('semicolon'):
            self._consume('semicolon')
            return '<{namespace}:{instruction} {params}/>'.format(
                namespace=namespace,
                instruction=instruction,
                params=params
            )
        elif self._next_token_is('curopen'):
            self._consume('curopen')
            
            output = '<{nmspc}:{inst} {params}>{prg}</{nmspc}:{inst}>'.format(
                nmspc=namespace,
                prg=self._read_program(),
                inst=instruction,
                params=params,
            )
            
            self._consume('curclose')

            return output
        else:
            raise UnexpectedToken(
                self._next_offset(),
                self._next_token(),
                'semicolon or curly brace'
            )

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

        if ':' not in parameter and parameter not in XSL_ALL_ATTRIBUTES:
            raise UnknownAttribute(self._next_offset(), parameter)

        self._consume('equals')
        _, value, _ = self._consume('string')

        value = multiple_replace(value, (
            ("&", "&amp;"),
            ("<", "&lt;"),
            (">", "&gt;"),
            (r'\"', "&quot;"),
            (r'\\', '\\')
        ))

        if self._next_token_is('comma'):
            self._consume('comma')

        return '{parameter}={value} '.format(parameter=parameter, value=value)

    def compile(self):
        """Compile the submitted list of tokens and generate an .xslt file"""
        return "<?xml version=\"1.0\"?>\n{0}".format(self._read_program())
