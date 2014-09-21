from lib import lexer_tools


class Preprocessor():
    """
    Removes whitespace and renames all variables and functions.
    Generates a map between hashes and line numbers to be used when working back from comparison results
    """

    def __init__(self, source, filename):
        self.line_map = self.create_line_map(source)
        self.processed_source = lexer_tools.normalize(source, filename)

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

