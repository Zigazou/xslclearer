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
    """Converts an .xsls file into an .xslt file
    
    It returns a tuple (return_code, output_xsls)
    return_code == 0 : compilation OK
    return_code == 1 : lexical analysis failed
    return_code == 2 : grammar analysis failed
    """
    xslstext = xsls_file.read()

    try:
        tokenizer = xsls.Tokenizer()

        skips = ['whitespace', 'comment', 'newline']
        tokens = [token for token in tokenizer.tokenize(xslstext, skips)]

        compiler = xsls.Compiler(tokens)
        return (0, compiler.compile())
    except xsls.TokenizerException as exception:
        row, column = offset_to_column_line(xslstext, exception.offset)
        return (1, "{message} at row {row}, column {column}".format(
            message=exception.message,
            row=row,
            column=column
        ))
    except xsls.CompilerException as exception:
        row, column = offset_to_column_line(xslstext, exception.offset)
        return (2, "{message} at row {row}, column {column}".format(
            message=exception.message,
            row=row,
            column=column
        ))

def main():
    """Interface between the operating system and the compiler"""

    # Determine where the input comes from
    if len(sys.argv) != 2:
        input_stream = sys.stdin
    else:
        input_stream = open(sys.argv[1])

    # Compile the XSLS input
    code, output = xsls_compile(input_stream)

    # Determine where the output has to go
    if code == 0:
        output_stream = sys.stdout
    else:
        output_stream = sys.stderr

    print(output, file=output_stream)
    sys.exit(code)

if __name__ == "__main__":
    main()

