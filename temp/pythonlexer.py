import temp.ply.ply.lex as lex


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
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)    
        return t

    # Define a rule so we can track line numbers.
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs).
    t_ignore  = ' \t'

    # Error handling rule.
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer.
    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
    
    # Test the lexer output.
    def test(self, data):
        out = ""
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            out += "<" + tok.type + ">"
        return out
            
# Build the lexer and try it out.
m = PythonLexer()
# Test it.
print(m.test("3 + 4"))