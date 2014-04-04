#!/usr/bin/env python
"""Exceptions generated by the XSLSCompiler"""

class XSLSCompilerException(Exception):
    """Exception generated when the XSLSCompiler encounters a syntax error"""
    def __init__(self, message, offset):
        self.offset = offset
        Exception.__init__(self, message)

class XSLSUnexpectedToken(XSLSCompilerException):
    """Exception generated when the XSLSCompiler was expecting something
    different"""
    def __init__(self, offset, unexpected, expected):
        self.unexpected = unexpected
        self.expected = expected
        message = "Unexpected %s, was expecting %s" % (
            self.unexpected,
            self.expected
        )
        XSLSCompilerException.__init__(self, message, offset)

class XSLSUnknownIdentifier(XSLSCompilerException):
    """Exception generated when the XSLSCompiler encounters an unknown
    identifier"""
    def __init__(self, offset, identifier):
        self.identifier = identifier
        message = "Unknown identifier %s" % (self.identifier, )
        XSLSCompilerException.__init__(self, message, offset)

class XSLSUnknownAttribute(XSLSCompilerException):
    """Exception generated when the XSLSCompiler encounters an unknown
    attribute"""
    def __init__(self, offset, attribute):
        self.attribute = attribute
        message = "Unknown attribute %s" % (self.attribute, )
        XSLSCompilerException.__init__(self, message, offset)

class XSLSAmbiguousIdentifier(XSLSCompilerException):
    """Exception generated when the XSLSCompiler encounters an ambiguous
    identifier"""
    def __init__(self, offset, identifier):
        self.identifier = identifier
        message = "Ambiguous identifier %s" % (self.identifier, )
        XSLSCompilerException.__init__(self, message, offset)

class XSLSNoMoreTokenException(Exception):
    """Exception generated when the XSLSCompiler excpected another token
    but there was none available"""
    pass
