import datetime
from itertools import groupby, combinations
from operator import itemgetter
from app.models import Submission


class Comparator:
    def __init__(self, submission_list, compare_history=False, comparison_year=2012):
        """
        The process is as follows:
            get fingerprints -> compare
        :param submission_list: A list containing elements of type Submission(Model)
        """

        # The minimum number of consecutive matched lines to consider
        self.min_lines_matched = 3
        # The number of lines in a larger, matching block which are allowed to not match but still be included 
        # This is for when someone adds a comment in the middle of something they copied
        self.separation_allowance = 3
        # The minimum percentage match which we care about
        self.match_threshold = 10

        # this report object should contain dictionaries of the form
        # {filename_1, filename_2, percent_match, line_matches}
        self.report = []

        for sub_a, sub_b in combinations(submission_list, 2):
            if sub_a.user_id == sub_b.user_id:
                break
            result = self.get_result_dict(sub_a, sub_b)
            if result["percent_match"] > self.match_threshold:
                self.report.append(result)

        # Compare to historical data
        if compare_history:
            history_list = Submission.objects.filter(date__gte=datetime.date(comparison_year, 1, 1))\
                                             .exclude(submission_id=submission_list[0].submission_id)
            for submission in history_list:
                submission.fingerprint = eval(submission.fingerprint)

            for sub in submission_list:
                for hist_sub in history_list:
                    if sub.user_id == hist_sub.user_id:
                        break
                    print("Comparing to history with ID {0}".format(hist_sub.submission_id))
                    result = self.get_result_dict(sub, hist_sub)
                    if result["percent_match"] > self.match_threshold:
                        self.report.append(result)

    def get_result_dict(self, sub_a, sub_b):
        result = {"file_1": sub_a.id,
                  "file_2": sub_b.id,
                  "line_matches": self.compare_fingerprints(sub_a.fingerprint, sub_b.fingerprint),
                  "submission_id_a": sub_a.submission_id,
                  "submission_id_b": sub_b.submission_id}
        result["percent_match"] = self.calculate_percent_match(result["line_matches"], sub_a, sub_b)
        return result


    @staticmethod
    def calculate_percent_match(line_ranges, sub_a, sub_b):
        """
        :param line_ranges: A list of tuples, containing matching lines
        :return: A percentage of the number of lines matched in the smaller file.
        This does not include blank lines, because we don't match on blank lines and want to me consistent
        """
        num_matches_1 = sum(len(x[0]) for x in line_ranges)
        num_lines_1 = len([x for x in sub_a.file_contents.split("\n") if x != ""])
        percent_1 = num_matches_1/num_lines_1

        num_matches_2 = sum(len(x[1]) for x in line_ranges)
        num_lines_2 = len([x for x in sub_b.file_contents.split("\n") if x != ""])
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

        if len(final_matches) < 2:
            return final_matches

        # we now want to include lines which may be splitting big chunks of copied blocks because they didn't match
        pos = 1
        while True:
            a_current = final_matches[pos][0]
            b_current = final_matches[pos][1]
            a_prev = final_matches[pos-1][0]
            b_prev = final_matches[pos-1][1]

            grace_a = a_current[0] - a_prev[-1]
            grace_b = b_current[0] - b_prev[-1]

            if grace_a <= self.separation_allowance and grace_b <= self.separation_allowance:
                lines_a = final_matches[pos-1][0] + list(range(a_prev[-1]+1, a_current[0])) + a_current
                lines_b = final_matches[pos-1][1] + list(range(b_prev[-1]+1, b_current[0])) + b_current
                final_matches[pos-1] = (lines_a, lines_b)
                del final_matches[pos]
            else:
                pos += 1
            if pos >= len(final_matches):
                break

        return final_matches

