import sys
from Tokenizer import Tokenizer


class CompileEngine:
    def __init__(self, T = Tokenizer):
        self.T = T
        self.currentToken = ""
        self.currentTokenType = ""
        # self.output = ""

    # The following are suggested helper functions.
    # You need not use them if you have other ideas
    # about getting this done.

    def process(self, str):
        if self.currentToken == str:
            self.printXMLToken()
            self.T.advance()
        else:
            print("Syntax error")
            self.T.advance()

    def printXMLToken(self):
        token = self.T.getToken()
        type = self.T.getType()
        print(f"<{type}> {token} </{type}>")

    def checkToken(self, tokens):
        """
        Checks to see if the current token found in 
        self.T.getToken()
        is in the tuple tokens.
        Print the token in appropriate XML if it is.
        Give an error message and halt if it is not.
        """
        self.currentToken = self.T.getToken()
        if type(tokens) is not tuple:
            tokens = (tokens,)
        if(self.T.getToken()) in tokens:
            self.process(self.T.getToken)
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

    # def compile(self):
    #     compiled_Code = ""
    #     self.T.advance()

    def compileClass(self):
        """
        Compiles <class> :=
            'class' <class-name> '{' <class-var-dec>* <subroutine-dec>* '}'

        The tokenizer is expected to be positionsed at the beginning of the
        file.
        """
        print("<class>")
        self.checkToken(("class",))
        self.checkType(("identifier",))  # lowercase this
        self.checkToken("{")
        while self.T.getToken() in ("static", "field"):
            self.compileClassVarDec()
        while self.T.getToken() in ("constructor", "function", "method"):
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
            self.checkToken((";"))
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
            self.checkToken(("void"))
        else:
            self.checkType((self.T.getType))
        self.checkToken(self.T.getToken())  # compile subroutine name
        self.checkToken(("("))
        self.compileParameterList()
        self.checkToken((")"))
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
        if self.T.getToken() != ")":
            self.checkType((self.T.getType()))
            self.checkToken((self.T.getToken()))
            while self.T.getToken == ",":
                self.checkToken((","))
                self.checkType(self.T.getType())
                self.checkToken(self.T.getToken())
        print("</parameterList>")

    def compileSubroutineBody(self):
        """
        Compiles <subroutine-body> :=
            '{' <var-dec>* <statements> '}'
        """
        print("<subroutineBody>")
        self.process('{')
        while self.T.getToken() in ('var'):
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
        self.checkType((self.T.getType()))
        self.checkToken((self.T.getToken()))
        while self.T.getToken() == ',':
            self.checkToken((","))
            self.checkToken(self.T.getToken())
        self.checkToken((";"))
        print("</varDec>")

    def compileStatements(self):
        """
        Compiles <statements> := (<let-statement> | <if-statement> |
            <while-statement> | <do-statement> | <return-statement>)*
        """
        print("<statements>")
        while self.T.getToken() in ('let', 'if', 'while', 'do', 'return'):
            if self.T.getToken == 'let':
                self.compileLet()
            if self.T.getToken == 'if':
                self.compileIf()
            if self.T.getToken == 'while':
                self.compileWhile()
            if self.T.getToken == 'do':
                self.compileDo()
            if self.T.getToken == 'return':
                self.compileReturn()
        print("</statements>")

    def compileLet(self):
        """
        Compiles <let-statement> :=
            'let' <var-name> ('[' <expression> ']')? '=' <expression> ';'
        """
        print("<letStatement>")
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
        print("</doStatment>")

    def compileIf(self):
        """
        Compiles <if-statement> :=
            'if' '(' <expression> ')' '{' <statements> '}' ( 'else'
            '{' <statements> '}' )?
        """
        print("<ifStatement>")
        self.checkToken("if")
        self.checkToken('(')
        print("</ifStatement>")

    def compileWhile(self):
        """
        Compiles <while-statement> :=
        'while' '(' <expression> ')' '{' <statements> '}'
        """
        print("<whileStatement>")

        print("</whileStatement>")

    def compileDo(self):
        """
        Compiles <do-statement> := 'do' <subroutine-call> ';'

        <subroutine-call> := (<subroutine-name> '(' <expression-list> ')') |
            ((<class-name> | <var-name>) '.' <subroutine-name> '('
            <expression-list> ')')

        <*-name> := <identifier>
        """
        print("<doStatement>")

        print("</doStatement>")

    def compileReturn(self):
        """
        Compiles <return-statement> :=
            'return' <expression>? ';'
        """
        print("<returnStatement>")

        print("</returnStatement>")


# The following are not LL(1) and are not part of the initial assignment

    def compileExpression(self):
        """
        Compiles <expression> :=
            <term> (op <term>)*
        """
        print("<expression>")
        print("</expression>")

    def compileExpressionList(self):
        """
        Compiles <expression-list> :=
            (<expression> (',' <expression>)* )?
        """

        print("<expressionList>")
        print("</expressionList>")

    def compileTerm(self):
        """
        Compiles a <term> :=
            <int-const> | <string-const> | <keyword-const> | <var-name> |
            (<var-name> '[' <expression> ']') | <subroutine-call> |
            ( '(' <expression> ')' ) | (<unary-op> <term>)
        """
        print("<term>")
        print("</term>")
