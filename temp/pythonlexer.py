import ply.ply.lex as lex


class PythonLexer:
    
    processedoutput = ""
    
    # List of keywords.
    keywords = {
        'False' : 'False',
        'None' : 'None',
        'True' : 'True',
        'and' : 'and',
        'as' : 'as',
        'assert' : 'assert',
        'break' : 'break',
        'class' : 'class',
        'continue' : 'continue',
        'def' : 'def',
        'del' : 'del',
        'elif' :'elif',
        'else' : 'else',
        'except' : 'except',
        'finally' : 'finally',
        'for' : 'for',
        'from' : 'from',
        'global' : 'global',
        'if' : 'if',
        'import' : 'import',
        'in' : 'in',
        'is' : 'is',
        'lambda' : 'lambda',
        'nonlocal' : 'nonlocal',
        'not' : 'not',
        'or' : 'or',
        'pass' : 'pass',
        'raise' : 'raise',
        'return' : 'return',
        'try' : 'try',
        'while' : 'while',
        'with' : 'with',
        'yield' : 'yield'   
        }
    
    # List of token names.
    tokens = ['V', 'COMMENT', 'STRING'] + list(keywords.values())
    
    # A regular expression rule for identifiers.
    def t_V(self,t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        # Check for keywords.
        t.type = self.keywords.get(t.value, 'V')
        return t
        
    # A regular expression rule for comments.
    def t_COMMENT(self,t):
        r'\#.*'
        self.processedoutput += t.value
        pass
    
    # A regular expression rule for strings.
    def t_STRING(self,t):
        r'\".*'
        self.processedoutput += t.value
        pass
            
    # Rule to handle characters that are not defined as tokens.
    def t_error(self,t):
        self.processedoutput += t.value[0]
        t.lexer.skip(1)
        
    # Build the lexer.
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
    
    # Test the lexer output.
    def test(self,data):         
        self.lexer.input(data)     
        while True:
            tok = self.lexer.token()
            if not tok: break
            self.processedoutput += tok.type
        return self.processedoutput

# Read a Python source file.
file = open("a.py", "r")
rawsourcecode = file.read()
file.close()
            
# Create a PythonLexer object.
m = PythonLexer()
# Build the PythonLexer object.
m.build()    

# Test the PythonLexer object.
processedsourcecode = m.test(rawsourcecode)
print(processedsourcecode)


    
    
