from io import StringIO
import tokenize


def preprocess(source):
    """
    :return: The 'source' without whitespace, comments, docstrings or blank lines.
    """  
    io_obj = StringIO(source)
    out = ""

    for tok in tokenize.generate_tokens(io_obj.readline):
        token_type = tok[0]
        token_string = tok[1]

        # comments:
        if token_type == tokenize.COMMENT:
            pass
        # docstrings:
        elif token_type == tokenize.STRING:
            if token_string[0:3] == r'"""' and token_string[-3:] == r'"""':
                print("X:", token_string)
                out += "\n"*token_string.count("\n")
            else:
                out += token_string
        # whitespace
        else:
            out += token_string.replace(" ", "")

    # eat the last extra newline
    return out[:-1]


def normalize(filename):
    c = open(filename, "r")
    source_c = c.read()
    c.close()
    out = preprocess(source_c)
    return out
    

