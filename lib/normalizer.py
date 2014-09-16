from pygments import lex, format
from pygments.token import Token
from pygments.formatter import Formatter
from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound


def normalize(source, filename):
    try:
        lexer = get_lexer_for_filename(filename)
        #source = reformat(source, lexer, NormalizeFormatter())
    except ClassNotFound:
        print("no suitable lexer found")

    finally:
        source = source.replace(" ", "").replace("\n", "")
    return source


def reformat(code, lexer, formatter):
    return format(lex(code, lexer), formatter)


class NormalizeFormatter(Formatter):
    """
    Custom formatter for Pygments package.
    Requires Pygments to be installed as a dependency.
    """
    def format(self, tokensource, outfile):
        for ttype, value in tokensource:
            if ttype in [Token.Name, Token.Name.Function, Token.Name.Attribute]:
                outfile.write("V")
            else:
                outfile.write(value)