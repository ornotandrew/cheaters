# Code adapted from http://code.activestate.com/recipes/576704/
from io import StringIO
import tokenize

def preprocessor(source):
    """
    Returns 'source' without comments, docstrings and blank lines.
    
    **Note**: Uses Python's built-in tokenize module to great effect.

    Example:

    .. code-block:: python

        def noop(): # This is a comment
            '''
            Does nothing.
            '''
            pass # Don't do anything

    Will become:

    .. code-block:: python
        def noop():
            pass
    """  
    io_obj = StringIO(source)
    out = ""
    prev_toktype = tokenize.INDENT
    last_lineno = -1
    last_col = 0
    
    for tok in tokenize.generate_tokens(io_obj.readline):
        token_type = tok[0]
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]
        
        # The following two conditionals preserve indentation.
        # This is necessary, because tokenize.untokenize() is not being used due 
        # to the fact that it results in code with extensive amounts of 
        # oddly-placed whitespace.

      #  if start_line > last_lineno:
       #     last_col = 0;
        #if(start_col > last_col):
         #   out += (" " * (start_col - last_col))

        # Remove comments:
        if token_type == tokenize.COMMENT:
            pass
        # This series of conditionals removes docstrings:
        elif token_type == tokenize.STRING:
            if prev_toktype != tokenize.INDENT:
        # This is likely a docstring; double-check whether not inside an 
        # operator:
                if prev_toktype != tokenize.NEWLINE:
                    # Note regarding NEWLINE vs NL: The tokenize module
                    # differentiates between newlines that start a new statement
                    # and newlines inside of operators such as parens, brackets,
                    # and curly braces. Newlines inside of operators are
                    # NEWLINE and newlines that start new code are NL.
                    # Catch whole-module docstrings:
                    if start_col > 0:
                        # Unlabelled indentation means inside an operator
                        out += token_string
                    # Note regarding the INDENT token: The tokenize module does
                    # not label indentation inside of an operator (parens, 
                    # brackets, and curly braces) as actual indentation.
                    # For example:
                    # def foo():
                    #     "The spaces before this docstring are tokenize.INDENT"
                    #     test = [
                    #         "The spaces before this string do not get a token"
                    #     ]
        else:
            out += token_string.replace(" ", "")
        prev_toktype = token_type
        last_col = end_col
        last_lineno = end_line
    # Remove all blank lines (including spaces):
    #out = "".join([x for x in out.strip().splitlines(True) if x.strip("\r\n").strip()])
    return out

def main():
    
    c = open("c.py", "r")
    source_c = c.read()
    c.close()
    out = preprocessor(source_c)
    print(out)
    
main() 
