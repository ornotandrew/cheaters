from itertools import groupby, combinations
from operator import itemgetter


class Comparator:
    def __init__(self, submission_list):
        """
        The process is as follows:
            get fingerprints -> compare
        :param submission_list: A list containing elements of type Submission(Model)
        """
        self.min_lines_matched = 3
        self.match_threshold = 10

        # this report object should contain dictionaries of the form
        # {filename_1, filename_2, percent_match, line_matches}
        self.report = []

        for sub_1, sub_2 in combinations(submission_list, 2):
            result = {"file_1": sub_1.id, "file_2": sub_2.id}
            result["line_matches"] = self.compare_fingerprints(sub_1.fingerprint, sub_2.fingerprint)
            result["percent_match"] = self.calculate_percent_match(result["line_matches"], sub_1, sub_2)
            if result["percent_match"] > self.match_threshold:
                self.report.append(result)
            # TODO: Compare to historical data



    @staticmethod
    def calculate_percent_match(line_ranges, sub_1, sub_2):
        """
        :param line_ranges: A list of tuples, containing matching lines
        :return: A percentage of the number of lines matched in the smaller file.
        This does not include blank lines, because we don't match on blank lines and want to me consistent
        """
        num_matches_1 = sum(len(x[0]) for x in line_ranges)
        num_lines_1 = len([x for x in sub_1.file_contents.split("\n") if x != ""])
        percent_1 = num_matches_1/num_lines_1

        num_matches_2 = sum(len(x[1]) for x in line_ranges)
        num_lines_2 = len([x for x in sub_2.file_contents.split("\n") if x != ""])
        percent_2 = num_matches_2/num_lines_2

        return int(max(percent_1, percent_2)*100)

    def compare_fingerprints(self, f_1, f_2):
        """
        :param f_1: Fingerprint A, containing a list containing elements -> [hash, [line_numbers]]
        :param f_2: see Fingerprint A
        :return: A list of the form [(line range in A, line range in B),...]
        """

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
        final_matches = []
        matches_a = [x[0] for x in all_matches]
        # iterate over consecutive sections in A
        for k, g in groupby(enumerate(matches_a), lambda t: t[0]-t[1]):
            match_range_a = list(map(itemgetter(1), g))

            # find the consecutive line matches in a over the threshold
            if len(match_range_a) >= self.min_lines_matched:
                match_temp = [x[1] for x in all_matches if x[0] in match_range_a]

                # iterate over consecutive sections in B
                for h, j in groupby(enumerate(match_temp), lambda t: t[0]-t[1]):
                    match_range_b = list(map(itemgetter(1), j))

                    # find the consecutive line matches in a over the threshold
                    if len(match_range_b) >= self.min_lines_matched:
                        final_matches.append((match_range_a, match_range_b))
                        # we only want one match in B for each match in A
                        break

        return final_matches

