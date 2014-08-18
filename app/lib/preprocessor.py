from io import StringIO
import tokenize


class Preprocessor():

    def __init__(self, filename):
        file = open(filename, "r")
        self.original_source = file.read()
        file.close()
        self.line_map = self.create_line_map(self.original_source)
        self.processed_source = self.normalize(self.original_source)

    def create_line_map(self, source):
        """
        Generates a map which will tell you what line you are on, given your index in file contents
        Your index is the number of your current character, not counting any newlines
        :param source: The original source code, as a string
        :return: The generated map
        """

        line_map = []
        if source[0] != "\n":
            line_map.append(1)
        current_line = 1

        for i in range(1, len(source)):
            if source[i-1] == "\n":
                current_line += 1
            if source[i] != "\n" and source[i] != " ":
                line_map.append(current_line)
        return line_map


    def normalize(self, source):
        """
        :return: The 'source' without whitespace or blank lines.
        """
        io_obj = StringIO(source)
        out = ""

        for tok in tokenize.generate_tokens(io_obj.readline):
            # token_type = tok[0]
            token_string = tok[1]
            out += token_string.replace(" ", "").replace("\n", "")
        return out
