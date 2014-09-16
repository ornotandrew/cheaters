from pygments import lex, format

from pygments.formatter import Formatter
from pygments.lexers import get_lexer_for_filename
from pygments.token import Token
from pygments.util import ClassNotFound


def normalize(source, filename):
    try:
        lexer = get_lexer_for_filename(filename)
        source = reformat(source, lexer, NormalizeFormatter())
    except ClassNotFound:
        print("no suitable lexer found")
    finally:
        source = source.replace(" ", "").replace("\n", "")
    return source


def reformat(code, lexer, formatter):
    return format(lex(code, lexer), formatter)


class NormalizeFormatter(Formatter):
    def format(self, tokensource, outfile):
        for ttype, value in tokensource:
            if ttype in [Token.Name.Function]:
                outfile.write("F")
            elif ttype in [Token.Name]:
                outfile.write("V")
            else:
                outfile.write(value)

filename = "c"
#source = open(filename, "r").read()
print(normalize("test test", filename))