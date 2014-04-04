#!/usr/bin/env python
"""This compile .xsls files into .xslt files"""

from XSLSCompilerException import (
    XSLSUnexpectedToken,
    XSLSUnknownIdentifier, 
    XSLSUnknownAttribute,
    XSLSAmbiguousIdentifier,
    XSLSNoMoreTokenException
)

from keywords.xslt_attributes import XSLT_ATTRIBUTES
from keywords.xslt_tags import XSLT_TAGS
from keywords.xsl_fo_attributes import XSL_FO_ATTRIBUTES
from keywords.xsl_fo_tags import XSL_FO_TAGS

XSL_ALL_TAGS = XSLT_TAGS + XSL_FO_TAGS
XSL_ALL_ATTRIBUTES = XSLT_ATTRIBUTES + XSL_FO_ATTRIBUTES

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
        tokname, _, _ = self._next_token()
        
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
            raise XSLSUnexpectedToken(
                self._next_offset(),
                self._next_token(),
                name                
            )

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
            raise XSLSUnexpectedToken(
                self._next_offset(),
                self._next_token(),
                'identifier or inplace'
            )

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

        if ':' not in instruction and instruction not in XSL_ALL_TAGS:
            raise XSLSUnknownIdentifier(self._next_offset(), instruction)

        params = self._read_parameters()

        # Guess the namespace for the given instruction
        if ':' in instruction:
            namespace = instruction.split(':')[0]
            instruction = instruction.split(':')[1]
        else:
            if instruction in XSLT_TAGS and instruction in XSL_FO_TAGS:
                raise XSLSAmbiguousIdentifier(
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
            return '<%s:%s %s/>' % (namespace, instruction, params)
        elif self._next_token_is('curopen'):
            self._consume('curopen')
            
            program = self._read_program()

            output = '<%s:%s %s>%s</%s:%s>' % (
                namespace, instruction, params,
                program,
                namespace, instruction
            )
            
            self._consume('curclose')

            return output
        else:
            raise XSLSUnexpectedToken(
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
            raise XSLSUnknownAttribute(self._next_offset(), parameter)

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
