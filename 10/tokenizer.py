import re
import sys
import os

keywords = ['boolean', 'char', 'class', 'constructor', 'do', 'else',
            'false', 'field', 'function', 'if', 'int', 'let', 'method',
            'null', 'return', 'static', 'this', 'true', 'var', 'void', 'while'
            ]

symbols = '{}()[].,;+-*/&|<>=~'
numberChars = '0123456789'
numberStart = numberChars
identStart = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
identChars = identStart + numberChars


def removeComments(f):
    file = open(f, 'r')
    jack_code = file.read()

    # remove multline comments
    jack_code = re.sub(r'/\*\*.*?\*/', '', jack_code)
    # /\*\*  == /** (backslashes escape special meaning of *)
    # .*?    == matches any character (the charaters in between the comment indicators
    # \*/    == */

    # remove single line comments
    jack_code = re.sub(r'//.*', '', jack_code)

    file.close()
    return jack_code


def Main(f):
    f = f.strip()
    code_lines = f.splitlines()

    tokens = []
    for line in code_lines:
        # OG: line_tokens = re.split(r'(\(|\)|,|;|\.|\s)', line)
        line_tokens = re.split(r'(\(|\)|\[|\]|,|;|\.|\s|\".*?\")', line)
        # (        \(  |  \)  |  ,  |  ;  |  \.  |  \s  |  \".*?\"        )
        # \ is used to escape the special meaning of the character
        #       - It is needed for the parentheses and the period becuase
        #         they each have meaning within this re statement
        #
        # \( and \) take parentheses as tokens
        # , ; and \. take commas, semicolons, and periods as tokens
        # /s       takes spaces and whitesapce as tokens
        # \".*?\"  takes everything inbetween double quotations and makes
        #          it one big token including the quotations

        # Below prevents empty string tokens and whitespace tokens from being added to tokens list
        for token in line_tokens:
            if token != '' and not token.isspace():
                tokens.append(token)

    # tokens is now a list of all the individual tokens we want to read

    xml_code = '<tokens>\n'
    for token in tokens:

        if token in keywords:
            xml_code += '<keyword> ' + str(token) + ' </keyword>\n'

        elif token in symbols:
            if token == '>':
                xml_code += '<symbol> ' + '&gt;' + ' </symbol>\n'
            elif token == '<':
                xml_code += '<symbol> ' + '&lt;' + ' </symbol>\n'
            elif token == '&':
                xml_code += '<symbol> ' + '&amp;' + ' </symbol>\n'
            else:
                xml_code += '<symbol> ' + str(token) + ' </symbol>\n'

        elif '"' in token:
            token = token.replace('"', '')
            xml_code += '<stringConstant> ' + str(token) + ' </stringConstant>\n'

        elif token.isnumeric():
            xml_code += '<integerConstant> ' + str(token) + ' </integerConstant>\n'

        else:
            xml_code += '<identifier> ' + str(token) + ' </identifier>\n'
# end of file for xml codeF
    xml_code += '</tokens>\n'
    return xml_code

infile = sys.argv[1]
xmlFile = infile.replace(".jack", "T.xml")

commentsRemoved = removeComments(infile)
f = open(xmlFile, 'a')
f.write(Main(commentsRemoved))
f.close()
