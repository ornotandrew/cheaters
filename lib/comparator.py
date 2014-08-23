from itertools import groupby
from operator import itemgetter


class Comparator:

    def __init__(self, submission_list):
        """
        The process is as follows:
            get fingerprints -> compare
        :param submission_list: A list containing elements of type Submission(Model)
        """
        self.min_lines_matched = 3

        # this report object should contain dictionaries of the form
        # {filename_1, filename_2, percent_match, line_matches}
        self.report = []

        num_submissions = len(submission_list)

        for i in range(num_submissions):
            # compare to everything to the right
            for j in range(1, num_submissions-i):
                submission_1 = submission_list[i]
                submission_2 = submission_list[i+j]
                result = {"file_1": submission_1.id, "file_2": submission_2.id}
                result["line_matches"] = self.compare_fingerprints(submission_1.fingerprint, submission_2.fingerprint)
                result["percent_match"] = self.calculate_percent_match(result["line_matches"], submission_1, submission_2)
                self.report.append(result)
            # TODO: Compare to historical data

    @staticmethod
    def calculate_percent_match(line_matches, submission_1, submission_2):
        """
        :param line_matches: A list of tuples, containing matching lines
        :return: A percentage of the number of lines matched in the smaller file.
        This does not include blank lines, because we don't match on blank lines and want to me consistent
        """
        num_matches = len(line_matches)
        num_lines_1 = len([x for x in submission_1.file_contents.split("\n") if x != ""])
        num_lines_2 = len([x for x in submission_2.file_contents.split("\n") if x != ""])

        return int(num_matches/min(num_lines_1, num_lines_2)*100)

    def compare_fingerprints(self, f_1, f_2):
        """
        :param f_1: Fingerprint A, containing a list containing elements -> [hash, [line_numbers]]
        :param f_2: see Fingerprint A
        :return: A list of the form [(line in A, line in B),...]
        """

        result = []

        # dict_f_1 = self.make_dict(f_1)
        # dict_f_2 = self.make_dict(f_2)
        dict_f_1 = dict(f_1)
        dict_f_2 = dict(f_2)

        # we can now get a list of strings of hashes which match
        hash_matches = set(dict_f_1.keys()) & set(dict_f_2.keys())

        # and construct a list of unique tuples of matching lines -> [(line in a, line in b), ..]
        all_matches = []
        for match in hash_matches:
            all_matches += zip(dict_f_1[match], dict_f_2[match])
        all_matches = sorted(list(set(all_matches)))

        # we now want to only show cases where there are a few lines matched consecutively
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
        result = [x for x in all_matches if x[0] in final_matches_a or x[1] in final_matches_b]

        return result

    @staticmethod
    def make_dict(arg):
        """
        Does exactly what dict(arg) would do, but adds to existing entries rather than overwriting them
        :param arg: Anything of the form [key, value]
        :return: A dictionary, with the values for one key joined together as a list
        """
        result = {}
        for elem in arg:
            if not elem[0] in result.keys():
                result[elem[0]] = elem[1]
            else:
                print("{0}:{1} exists. adding {2}".format(elem[0], result[elem[0]], elem[1]))
                result[elem[0]] += elem[1]
        return result