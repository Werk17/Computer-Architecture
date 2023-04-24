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


class Tokenizer:

    def __init__(self, infile):
        infile = self.removeComments(infile)
        infile = infile.strip()
        self.code_lines = infile.splitlines()
        self.tokens = []
        self.keywords = keywords
        self.symbols = symbols
        self.numberChars = numberChars
        self.numberStart = numberStart
        self.identStart = identStart
        self.identChars = identChars
        self.curr_token = None
        self.token_type = None
        self.token_index = -1
        self.tokenize()

    def tokenize(self):
        # tokens = []
        for line in self.code_lines:
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
                    self.tokens.append(token)

            # tokens is now a list of all the individual tokens we want to read

    def removeComments(self, f):
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

    def hasMoreTokens(self):
        return self.token_index < len(self.tokens) - 1

    def advance(self):
        if self.hasMoreTokens():
            self.token_index += 1
            self.curr_token = self.tokens[self.token_index]
            if self.curr_token in symbols:
                self.token_type = "symbol"
            elif self.curr_token.isdigit():
                self.token_type = "int_const"
            elif self.curr_token[0] == '"' and self.curr_token[-1] == '"':
                self.token_type = "string_const"
            elif self.curr_token in keywords:
                self.token_type = "keyword"
            else:
                self.token_type = "identifier"
        else:
            self.curr_token = ""
            self.token_type = ""

    def keyWords(self):
        return self.keywords

    def getType(self):
        return self.token_type

    def getToken(self):
        return self.curr_token


infile = sys.argv[1]
xmlFile = infile.replace(".jack", "T.xml")
tokenizer = Tokenizer(infile)
# commentsRemoved = removeComments(infile)
# outFile.close()

# code before compile engine came
# xml_code = '<tokens>\n'
# use while loop for has more tokens
# while(not self.hasMoreTokens()):
#     # advance to next token and do stuff
#     self.advance()

# for token in self.tokens:
#     self.curr_token = token

#     if token in keywords:
#         xml_code += '<keyword> ' + str(token) + ' </keyword>\n'
#         self.token_type = self.getType()

#     elif token in symbols:
#         self.token_type = self.getType()
#         if token == '>':
#             xml_code += '<symbol> ' + '&gt;' + ' </symbol>\n'
#         elif token == '<':
#             xml_code += '<symbol> ' + '&lt;' + ' </symbol>\n'
#         elif token == '&':
#             xml_code += '<symbol> ' + '&amp;' + ' </symbol>\n'
#         else:
#             xml_code += '<symbol> ' + str(token) + ' </symbol>\n'

#     elif '"' in token:
#         token = token.replace('"', '')
#         self.token_type = self.getType()
#         xml_code += '<stringConstant> ' + \
#             str(token) + ' </stringConstant>\n'

#     elif token.isnumeric():
#         self.token_type = self.getType()
#         xml_code += '<integerConstant> ' + \
#             str(token) + ' </integerConstant>\n'

#     else:
#         self.token_type = self.getToken()
#         xml_code += '<identifier> ' + str(token) + ' </identifier>\n'
# # end of file for xml codeF
# xml_code += '</tokens>\n'
# return xml_code
