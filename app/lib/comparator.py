from itertools import groupby
from operator import itemgetter
from app.lib.fingerprinter import Fingerprinter
from app.lib.preprocessor import Preprocessor


class Comparator:

    def __init__(self, filename_a, filename_b):
        """
        The process is as follows:
            get fingerprints -> compare
        :param fingerprint_list: A list containing elements of type {file_descriptor, fingerprint}
        """
        self.min_lines_matched = 3

        preprocessor_a = Preprocessor(filename_a)
        preprocessor_b = Preprocessor(filename_b)
        print_a = Fingerprinter(preprocessor_a)
        print_b = Fingerprinter(preprocessor_b)

        self.result = self.compare_fingerprints(print_a.fingerprint, print_b.fingerprint)

        # make result[0] a percentage of total lines, since we have the sources up here
        # we don't want to count blank lines, because we are not matching on blank lines
        # TODO: make this non-retarded and put it in the preprocessor
        num_lines_a = len([x for x in preprocessor_a.original_source.split("\n") if x != ""])
        num_lines_b = len([x for x in preprocessor_b.original_source.split("\n") if x != ""])
        self.result[0] = int(self.result[0]/min(num_lines_a, num_lines_b)*100)

    def compare_fingerprints(self, f_a, f_b):
        """
        :param f_a: Fingerprint A, containing it's hash and line numbers
        :param f_b: Fingerprint B, containing it's hash and line numbers
        :return: A list of the form [number of matching lines, [(line in A, line in B),...]]
        """

        result = [0, []]

        dict_f_a = dict(f_a)
        dict_f_b = dict(f_b)
        # we can now get a list of strings of hashes which match
        hash_matches = set(dict_f_a.keys()) & set(dict_f_b.keys())

        hash_map = {}
        for match in hash_matches:
            line_list_a = dict_f_a[match]
            line_list_b = dict_f_b[match]
            for i in range(len(line_list_a)):
                hash_map[str(1000*line_list_a[i]+line_list_b[i])] = (line_list_a[i], line_list_b[i])

        # we now want to only show cases where there are a few lines matched consecutively
        all_matches = sorted(list(hash_map.values()))
        matches_a = [x[0] for x in all_matches]
        final_matches_a = []
        # the following 2 lines were tearfully whispered by a great wizard
        # as he gave his life to aid the cause of Python
        # (it's one of the itertools examples in the docs)
        for k, g in groupby(enumerate(matches_a), lambda t: t[0]-t[1]):
            match_range = list(map(itemgetter(1), g))
            if len(match_range) >= self.min_lines_matched:
                final_matches_a += match_range
        # TODO: there's probably a clever way to do this...
        final_matches_b = [x[1] for x in all_matches if x[0] in final_matches_a]
        result[1] = [x for x in all_matches if x[0] in final_matches_a or x[1] in final_matches_b]

        result[0] = len(result[1])
        print(result)
        return result