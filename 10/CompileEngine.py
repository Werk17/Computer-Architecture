import sys
from Tokenizer import Tokenizer


class CompileEngine:
    def __init__(self, T=Tokenizer):
        self.infile = sys.argv[1]
        self.xmlFile = self.infile.replace(".jack", "T.xml")
        self.T = T(self.infile)
        self.currentToken = self.T.getToken()
        self.currentTokenType = self.T.getType()
        self.operators = '+-*/&|<>+'
        self.unaryOp = '-~'
        self.tokenIndex = 0

    # The following are suggested helper functions.
    # You need not use them if you have other ideas
    # about getting this done.

    def process(self, str):
        if self.currentToken == str:
            self.printXMLToken()
            self.T.advance()
            self.tokenIndex += 1
        else:
            print("Syntax error")
            self.T.advance()

    def printXMLToken(self):
        token = self.currentToken
        type = self.currentTokenType
        print(f"<{type}> {token} </{type}>")

    def checkToken(self, tokens):
        """
        Checks to see if the current token found in 
        self.T.getToken()
        is in the tuple tokens.
        Print the token in appropriate XML if it is.
        Give an error message and halt if it is not.
        """
        # this makes sure that these current values are updated everytime they are checked
        self.currentToken = self.T.getToken()
        self.currentTokenType = self.T.getType()

        if type(tokens) is not tuple:
            tokens = (tokens,)
        if(self.currentToken) in tokens:
            self.process(self.currentToken)
        else:
            print(f"Error: unexpected token {self.currentToken}")
            sys.exit()

    def checkType(self, expected_types):
        """
        Checks to see if the current type found in 
        self.T.getType()
        is in the tuple expected types.
        Print the token in appropriate XML and 
        advance to the next token if it is.
        Give an error message and halt if it is not.
        """
        # this makes sure that these current values are updated everytime they are checked
        self.currentToken = self.T.getToken()
        self.currentTokenType = self.T.getType()

        if expected_types is not tuple:
            expected_types = (expected_types,)
        if self.currentTokenType in expected_types:
            self.process(self.currentToken)
        else:
            print(
                f"Error: expected types {expected_types} but got {self.currentTokenType}")
            sys.exit()

    # The following are the compile functions that need to
    # be implemented. compileExpression has been withheld for a
    # future assignment

    def compile(self):
        self.T.advance()

    def compileClass(self):
        """
        Compiles <class> :=
            'class' <class-name> '{' <class-var-dec>* <subroutine-dec>* '}'

        The tokenizer is expected to be positionsed at the beginning of the
        file.
        """
        print("<class>")
        self.checkToken(("class",))
        self.checkType(("identifier",))
        self.checkToken("{")
        while self.currentToken in ["static", "field"]:
            self.compileClassVarDec()
        while self.currentToken in ["constructor", "function", "method"]:
            self.compileSubroutine()
        self.checkToken("}")
        print("</class>")

    def compileClassVarDec(self):
        """
        Compiles <class-var-dec> :=
            ('static' | 'field') <type> <var-name> (',' <var-name>)* ';'
        """
        print("<classVarDec>")
        self.checkToken(("static", "field"))
        self.checkType((self.currentTokenType))
        self.checkToken(self.currentToken)
        while self.currentToken == ",":
            self.checkToken((";",))
        print("</classVarDec>")

    def compileSubroutine(self):
        """
        Compiles <subroutine-dec> :=
            ('constructor' | 'function' | 'method') ('void' | <type>)
            <subroutine-name> '(' <parameter-list> ')' <subroutine-body>

        ENTRY: Tokenizer positioned on the initial keyword.
        EXIT:  Tokenizer positioned after <subroutine-body>.
        """
        print("<subroutineDec>")
        self.checkToken(("constructor", "function", "method"))
        if self.currentToken == "void":
            self.checkToken(("void",))
        else:
            self.checkType((self.currentTokenType))
        self.checkToken(self.currentToken)  # compile subroutine name
        self.checkToken(("(",))
        self.compileParameterList()
        self.checkToken((")",))
        self.compileSubroutineBody()
        print("</subroutineDec>")

    def compileParameterList(self):
        """
        Compiles <parameter-list> :=
            ( <type> <var-name> (',' <type> <var-name>)* )?

        ENTRY: Tokenizer positioned on the initial keyword.
        EXIT:  Tokenizer positioned after <subroutine-body>.
        """
        print("<parameterList>")
        if self.currentToken != ")":
            self.checkType((self.currentTokenType))
            self.checkToken((self.currentToken))
            while self.currentToken == ",":
                self.checkToken((","))
                self.checkType(self.currentTokenType)
                self.checkToken(self.currentToken)
        print("</parameterList>")

    def compileSubroutineBody(self):
        """
        Compiles <subroutine-body> :=
            '{' <var-dec>* <statements> '}'
        """
        print("<subroutineBody>")
        self.process('{')
        while self.currentToken in ('var'):
            self.compileVarDec()
        self.compileStatements()
        self.process('}')
        print("</subroutineBody>")

    def compileVarDec(self):
        """
        Compiles <var-dec> :=
            'var' <type> <var-name> (',' <var-name>)* ';'
        """
        print("<varDec>")
        self.checkToken(("var"))
        self.checkType((self.currentTokenType))
        self.checkToken((self.currentToken))
        while self.currentToken == ',':
            self.checkToken((","))
            self.checkToken(self.currentToken)
        self.checkToken((";"))
        print("</varDec>")

    def compileStatements(self):
        """
        Compiles <statements> := (<let-statement> | <if-statement> |
            <while-statement> | <do-statement> | <return-statement>)*
        """
        print("<statements>")
        while self.currentToken in ('let', 'if', 'while', 'do', 'return'):
            if self.currentToken == 'let':
                self.compileLet()
            if self.currentToken == 'if':
                self.compileIf()
            if self.currentToken == 'while':
                self.compileWhile()
            if self.currentToken == 'do':
                self.compileDo()
            if self.currentToken == 'return':
                self.compileReturn()
        print("</statements>")

    def compileLet(self):
        """
        Compiles <let-statement> :=
            'let' <var-name> ('[' <expression> ']')? '=' <expression> ';'
        """
        print("<letStatement>")
        self.checkToken('let')
        self.process(self.currentToken)
        if self.currentToken == '[':
            self.process('[')
            self.compileExpression()
            self.process(']')
        self.process('=')
        self.compileExpression()
        self.process(';')
        print("</letStatement>")

    def compileDo(self):
        """
        Compiles <do-statement> := 'do' <subroutine-call> ';'

        <subroutine-call> := (<subroutine-name> '(' <expression-list> ')') |
            ((<class-name> | <var-name>) '.' <subroutine-name> '('
            <expression-list> ')')

        <*-name> := <identifier>
        """
        print("<doStatement>")
        self.checkToken('do')
        self.compileSubroutineCall()
        self.process(';')
        print("</doStatment>")

    def compileIf(self):
        """
        Compiles <if-statement> :=
            'if' '(' <expression> ')' '{' <statements> '}' ( 'else'
            '{' <statements> '}' )?
        """
        print("<ifStatement>")
        self.checkToken('if')
        self.process('(')
        self.compileExpression()
        self.process(')')
        self.process('{')
        self.compileStatements()
        self.process('}')
        if self.currentToken == 'else':
            self.checkType('else')
            self.process('{')
            self.compileStatements()
            self.process('}')
        print("</ifStatement>")

    def compileWhile(self):
        """
        Compiles <while-statement> :=
        'while' '(' <expression> ')' '{' <statements> '}'
        """
        print("<whileStatement>")
        self.checkToken('while')
        self.process('(')
        self.compileExpression()
        self.process(')')
        self.process('{')
        self.compileStatements()
        self.process('}')
        print("</whileStatement>")

    def compileReturn(self):
        """
        Compiles <return-statement> :=
            'return' <expression>? ';'
        """
        print("<returnStatement>")
        self.checkToken('return')
        if self.currentToken != ';':
            self.compileExpression()
        self.process(';')
        print("</returnStatement>")


# The following are not LL(1) and are not part of the initial assignment


    def compileExpression(self):
        """
        Compiles <expression> :=
            <term> (op <term>)*
        """
        print("<expression>")
        self.compileTerm()
        # compile
        while self.currentToken in self.operators:
            self.process(self.currentToken)
            self.compileTerm()
        print("</expression>")

    def compileExpressionList(self):
        """
        Compiles <expression-list> :=
            (<expression> (',' <expression>)* )?
        """

        print("<expressionList>")
        if self.currentToken != ')':
            self.compileExpression()
            while self.currentToken == ",":
                self.process(self.currentToken)
                self.compileExpression()
        print("</expressionList>")

    def compileTerm(self):
        """
        Compiles a <term> :=
            <int-const> | <string-const> | <keyword-const> | <var-name> |
            (<var-name> '[' <expression> ']') | <subroutine-call> |
            ( '(' <expression> ')' ) | (<unary-op> <term>)
        """
        # self.operators = '+-*/&|<>+'
        # self.unaryOp = '-~'
        print("<term>")
        if self.currentTokenType == 'integerConstant':
            self.process(self.currentToken)
        elif self.currentTokenType == 'stringConstant':
            self.process(self.currentToken)
        elif self.currentTokenType == 'keyword':
            self.process(self.currentToken)
        elif self.currentTokenType in ('identifier', 'class'):
            if self.currentToken("(") or self.currentToken("."):
                self.compileSubroutineCall()
            elif self.currentToken == '[':
                self.compileExpression()
            else:
                self.process(self.currentToken)
        elif self.currentToken == '(':
            self.compileExpression()
        elif self.currentToken in self.unaryOp:
            self.process(self.currentToken)
            self.compileTerm()
        else:
            print(f"Unexpected token: {self.currentToken} in file")
        print("</term>")

    def compileSubroutineCall(self):
        """
        Compiles a subroutine call
        """
        if self.currentTokenType == "identifier":
            self.process(self.currentToken)
        else:
            self.process(self.currentToken)
            self.currentToken = self.T.getToken() # to make sure that the token updates 
            self.process(self.currentToken)
        self.compileExpressionList()
