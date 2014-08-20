import ply.ply.lex as lex

# Global variable.
outputstring = ""

class PythonLexer:
    # List of token names.
    tokens = (
       'NUMBER',
       'PLUS',
       'MINUS',
       'TIMES',
       'DIVIDE',
       'LPAREN',
       'RPAREN',
    )

    # Regular expression rules for simple tokens.
    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'
    t_DIVIDE  = r'/'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'

    # A regular expression rule with some action code.
    def t_NUMBER(self,t):
        r'\d+'
        t.value = int(t.value)    
        return t

    # Define a rule so we can track line numbers.
    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs).
    t_ignore  = ' \t'

    # Error handling rule.
    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer.
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
    
    # Test the lexer output.
    def test(self,data):         
        global outputstring
        self.lexer.input(data)     
        while True:
            tok = self.lexer.token()
            if not tok: break
            outputstring += "<" + tok.type + ">"
            
# Build the lexer and try it out.
m = PythonLexer()
# Build the lexer.
m.build()         
# Test it.
m.test("3 + 4")
print(outputstring)
    
    
    