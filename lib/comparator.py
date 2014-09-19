import datetime
from itertools import groupby, combinations
from operator import itemgetter
from app.models import Submission


class Comparator:
    def __init__(self, submission_list, **kwargs):
        """
        The process is as follows:
            get fingerprints -> compare
        :param submission_list: A list containing elements of type Submission(Model)
        """

        # The minimum number of consecutive matched lines to consider
        self.min_lines_matched = kwargs.get("min_lines_matched", 3)
        # The number of lines in a larger, matching block which are allowed to not match but still be included 
        # This is for when someone adds a comment in the middle of something they copied
        self.separation_allowance = kwargs.get("separation_allowance", 2)
        # The minimum percentage match which we care about
        self.match_threshold = kwargs.get("match_threshold", 10)

        # this report object should contain dictionaries of the form
        # {filename_1, filename_2, percent_match, line_matches}
        self.report = []

        for sub_a, sub_b in combinations(submission_list, 2):
            if sub_a.user_id == sub_b.user_id:
                break
            result = self.get_result_dict(sub_a, sub_b)
            if result["percent_match"] > self.match_threshold:
                self.report.append(result)

        comparison_year = kwargs.get("year", -1)
        compare_history = False if comparison_year is -1 else True

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

        # get all the unique values of a and b
        a_all = {}
        b_all = {}
        for l_range in line_ranges:
            for match in l_range:
                a_all[match[0]] = ""
                b_all[match[1]] = ""

        num_matches_a = len(a_all)
        num_lines_a = sub_a.file_contents.count("\n")
        percent_a = num_matches_a/num_lines_a

        num_matches_b = len(b_all)
        num_lines_b = sub_b.file_contents.count("\n")
        percent_b = num_matches_b/num_lines_b

        return int(max(percent_a, percent_b)*100)

    def compare_fingerprints(self, f_1, f_2):
        """
        :param f_1: Fingerprint A, containing a list containing elements -> [hash, [line_numbers]]
        :param f_2: see Fingerprint A
        :return: A 2D list of the form containing base elements [(line range in A, line range in B),...]
                 Which are then grouped with those which are consecutive to them
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

        # get rid of duplicate matches coming from the same line (keep the smallest corresponding line numbers)
        all_matches = self.filter_duplicates(all_matches)

        # interpolate the matches, then get rid of outliers
        all_matches = self.interpolate(all_matches)

        filtered_matches = self.remove_outlying_matches(all_matches)

        # group consecutive matches
        grouped_matches = self.group_matches(filtered_matches)

        return grouped_matches

    def interpolate(self, match_seq):
        """
        :param seq: A sorted list of tuples
        :return: The same list, but with 'gaps' filled in where the space between matches is sufficiently small
        """
        extra_matches = []
        for i in range(1, len(match_seq)):
            a_current, a_prev = match_seq[i][0], match_seq[i-1][0]
            b_current, b_prev = match_seq[i][1], match_seq[i-1][1]
            diff_a = a_current - a_prev
            diff_b = b_current - b_prev

            if 1 <= diff_a <= self.separation_allowance and 1 <= diff_b <= self.separation_allowance:
                for offset in range(1, max(diff_a, diff_b)):
                    extra_matches.append((a_prev+offset, b_prev+offset))

        return sorted(match_seq + extra_matches)

    @staticmethod
    def filter_duplicates(seq):
        """
        :param seq: A sorted list of tuples
        :return: The same list, but with duplicates in the first elemtnt removed
        Example, [(1, 1), (1, 2), (1, 3), (2, 2)] -> [(1, 1), (2, 2)]
        """
        result = [seq[0]]
        prev_a = seq[0][0]
        for i in range(1, len(seq)):
            if not seq[i][0] == prev_a:
                result.append(seq[i])
                prev_a = seq[i][0]
        return result

    def remove_outlying_matches(self, match_seq):
        """
        :param match_seq: An ordered list of tuples
        :return: The list, after removing elements which aren't in sufficiently large groups of consecutive numbers
        """
        lines_a, lines_b = [x[0] for x in match_seq], [x[1] for x in match_seq]
        accepted_a = self.remove_outlying_numbers(lines_a)
        accepted_b = self.remove_outlying_numbers(lines_b)

        result = []
        for match in match_seq:
            if match[0] in accepted_a and match[1] in accepted_b:
                result.append(match)

        return result

    def remove_outlying_numbers(self, seq):
        """
        :param seq: An ordered list of numbers
        :return: The list, after removing elements which aren't in sufficiently large groups of consecutive numbers
        """
        result = []
        for k, g in groupby(enumerate(sorted(list(set(seq)))), lambda t: t[0]-t[1]):
            temp = list(map(itemgetter(1), g))
            if len(temp) >= self.min_lines_matched:
                result += temp
        return result

    @staticmethod
    def group_matches(match_seq):
        """
        :param match_seq: An ordered list of matches, with no outliers
        :return: A 2D list containing matches grouped with ones which are consecutive in the first element
        """
        if len(match_seq) == 0:
            return []

        result = []
        current = [match_seq[0]]
        for i in range(1, len(match_seq)):
            # if the current match follows from the previous one (or is the same), add it to current (done on the A line)
            if match_seq[i][0] == match_seq[i-1][0]+1 or match_seq[i][0] == match_seq[i-1][0]:
                current.append(match_seq[i])
            # otherwise, we are finished with the current bucket
            else:
                result.append(current)
                current = [match_seq[i]]

        # include the last bucket
        result.append(current)

        return result