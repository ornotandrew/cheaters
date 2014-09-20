from pygments import lex, format
from pygments.token import Token
from pygments.formatter import Formatter
from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound


def normalize(source, filename):
    """
    :param source: raw source code
    :param filename: filename of the source code to use relevant lexer
    :return: normalized code, meaning all variable and method names were renamed
    and all whitespace removed
    """
    try:
        lexer = get_lexer_for_filename(filename)
        source = format(lex(source, lexer), NormalizeFormatter())

    except ClassNotFound:
        print("no suitable lexer found")

    finally:
        source = source.replace(" ", "").replace("\n", "")
    return source


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