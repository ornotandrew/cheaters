import datetime
from itertools import groupby, combinations
from operator import itemgetter
from app.models import Submission


class Comparator:
    def __init__(self, submission_list, compare_history=False, comparison_year=2012,
                 min_lines_matched=3, separation_allowance=2, match_threshold=10):
        """
        The process is as follows:
            get fingerprints -> compare
        :param submission_list: A list containing elements of type Submission(Model)
        """

        # The minimum number of consecutive matched lines to consider
        self.min_lines_matched = min_lines_matched
        # The number of lines in a larger, matching block which are allowed to not match but still be included 
        # This is for when someone adds a comment in the middle of something they copied
        self.separation_allowance = separation_allowance
        # The minimum percentage match which we care about
        self.match_threshold = match_threshold

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
        num_matches = sum(len(x) for x in line_ranges)
        num_lines_1 = sub_a.file_contents.count("\n")
        percent_1 = num_matches/num_lines_1

        num_lines_2 = sub_b.file_contents.count("\n")
        percent_2 = num_matches/num_lines_2

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
        match_ranges_a = self.get_ranges([x[0] for x in all_matches])
        match_ranges_b = self.get_ranges([x[1] for x in all_matches])

        final_matches = []
        for match in all_matches:
            if match[0] in match_ranges_a and match[1] in match_ranges_b:
                final_matches.append(match)

        if len(final_matches) < 2:
            return final_matches

        # we now want to include lines which may be splitting big chunks of copied blocks because they didn't match
        for pos in range(len(final_matches)):
            a_current = final_matches[pos][0]
            b_current = final_matches[pos][1]
            a_prev = final_matches[pos-1][0]
            b_prev = final_matches[pos-1][1]

            grace_a = a_current - a_prev
            grace_b = b_current - b_prev

            if grace_a <= self.separation_allowance and grace_b <= self.separation_allowance:
                for i in range(1, max(grace_a, grace_b)):
                    final_matches.append((a_prev+i, b_prev+i))

        # reconstruct the groups. we can now just look at a
        temp = sorted(final_matches)
        final_matches = []
        current_range = []
        for i in range(1, len(temp)):
            # don't add duplicate matches
            if temp[i][0] == temp[i-1][0]:
                continue
            # if the number of a is one more than the previous a, add the match to the current range
            elif temp[i][0] == temp[i-1][0]+1:
                current_range.append(temp[i])
            # otherwise, start a new current range
            else:
                if len(current_range) >= self.min_lines_matched:
                    final_matches.append(current_range)
                current_range = []
        # add the final range
        if len(current_range) >= self.min_lines_matched:
            final_matches.append(current_range)

        return final_matches

    def get_ranges(self, seq):
        ranges = []
        for k, g in groupby(enumerate(seq), lambda t: t[0]-t[1]):
            temp = list(map(itemgetter(1), g))
            # if len(temp) >= self.min_lines_matched:
            #     ranges += temp
            ranges += temp
        return ranges
