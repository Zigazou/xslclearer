#!/usr/bin/env python3
"""xslclearer compile .xsls files into .xslt files"""

import sys
import xsls

def offset_to_column_line(text, offset):
    """Convert an offset in a file to (row, column) coordinates"""
    if offset > len(text):
        return False

    lines = text.split('\n')

    row = 0
    column = offset
    for line_number in range(0, len(lines)):
        line_length = len(lines[line_number])

        if column < line_length:
            row = line_number
            break

        column -= line_length + 1

    return (row + 1, column + 1)

def xsls_compile(xsls_file):
    """Converts an .xsls file into an .xslt file"""
    xslstext = xsls_file.read()

    try:
        tokenizer = xsls.Tokenizer()

        skips = ['whitespace', 'comment', 'newline']
        tokens = [token for token in tokenizer.tokenize(xslstext, skips)]

        compiler = xsls.Compiler(tokens)
        return compiler.compile()
    except xsls.TokenizerException as exception:
        row, column = offset_to_column_line(xslstext, exception.offset)
        return "{message} at row {row}, column {column}".format(
            message=exception.message,
            row=row,
            column=column
        )
    except xsls.CompilerException as exception:
        row, column = offset_to_column_line(xslstext, exception.offset)
        return "{message} at row {row}, column {column}".format(
            message=exception.message,
            row=row,
            column=column
        )

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(xsls_compile(sys.stdin))
    else:
        print(xsls_compile(open(sys.argv[1])))
