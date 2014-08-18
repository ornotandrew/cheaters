from itertools import groupby
from operator import itemgetter
from app.lib.preprocessor import Preprocessor


class Comparator:
    """
    This class provides methods for comparing source files. It is a python implementation of hashing and "winnowing"
    very similar to MOSS (http://theory.stanford.edu/~aiken/moss/). Certain specifics in the algorithm have been set
    according to the whitepaper on MOSS, which available at the above URL.
    We define variables in such a way that:
        1. If there is a substring match at least as long as the guaranteed threshold, t, then this match is detected
        2. We do not detect any matches shorter than the noise threshold, n
    Point (2) is already guaranteed because we use n to generate the ngrams
    We can now define the 'window size', w = t - n + 1
    This guarantees point (1) above
    """

    def __init__(self, filename_a, filename_b):
        self.n = 10
        self.t = 15
        self.w = self.t - self.n + 1
        self.min_lines_matched = 3
        self.preprocessor_a = Preprocessor(filename_a)
        self.preprocessor_b = Preprocessor(filename_b)

    def compare(self):
        """
        The process here is as follows:
            normalize -> generate ngrams -> hash ngrams -> winnow -> compare
        :return: A list of the form [percentage match, [(line in A, line in B),...]]
        """

        ngrams_a = self.get_ngrams(self.preprocessor_a)
        ngrams_b = self.get_ngrams(self.preprocessor_b)
        hashes_a = self.get_hash_values(ngrams_a)
        hashes_b = self.get_hash_values(ngrams_b)
        fingerprint_a = self.winnow(hashes_a)
        fingerprint_b = self.winnow(hashes_b)

        result = self.compare_fingerprints(fingerprint_a, fingerprint_b)

        # make result[0] a percentage of total lines, since we have the sources up here
        # we don't want to count blank lines, because we are not matching on blank lines
        # TODO: make this non-retarded and put it in the preprocessor
        num_lines_a = len([x for x in self.preprocessor_a.original_source.split("\n") if x != ""])
        num_lines_b = len([x for x in self.preprocessor_b.original_source.split("\n") if x != ""])
        result[0] = int(result[0]/min(num_lines_a, num_lines_b)*100)

        return result

    def get_ngrams(self, preprocessor):
        """
        :param source: One long, continuous (normalized) string
        :param n: The minimum number of consecutive characters to be a match
        :return A list of the containing elements of the form [ngram, [lines the ngram appears on]]
        """
        source = preprocessor.processed_source
        ngrams = []

        for i in range(len(source)-self.n+1):
            line_range_raw = preprocessor.line_map[i:i+self.n]
            line_range = list(set([x for x in line_range_raw if line_range_raw.count(x) > 1]))
            ngrams.append([source[i:i+self.n], line_range])

        return ngrams

    def get_hash_values(self, ngram_list):
        """
        This replaces the ngrams with their hashes instead of making a new list
        :return: the original ngram_pairs, but now of the form [hash, [lines the ngram appears on]]
        """

        # run the first hash normally
        first_hash_in_prev_window = 0
        current_ngram = ngram_list[0][0]
        hash_value = 0
        for i in range(len(current_ngram)):
            hash_value += ord(current_ngram[i])*10**(len(current_ngram)-i-1)
            if i == 0:
                first_hash_in_prev_window = hash_value
        ngram_list[0][0] = hash_value

        # then use the rolling function
        for hash_index in range(1, len(ngram_list)):
            current_ngram = ngram_list[hash_index][0]
            temp = ord(current_ngram[0])*10**(len(current_ngram)-1)
            prev_hash = ngram_list[hash_index-1][0]
            ngram_list[hash_index][0] = (prev_hash - first_hash_in_prev_window)*10 + ord(ngram_list[hash_index][0][-1])
            first_hash_in_prev_window = temp

        return ngram_list

    def winnow(self, hashes):
        """
        We define variables in such a way that:
            1. If there is a substring match at least as long as the guaranteed threshold, t, then this match is detected
            2. We do not detect any matches shorter than the noise threshold, n
        Point (2) is already guaranteed because we use n to generate the ngrams
        We can now define the 'window size', w = t - k + 1
        This guarantees point (1) above

        In each window select the minimum hash value. If possible break ties by selecting
        the same hash as the window one position to the left. If not, select the rightmost
        minimal hash. Save all selected hashes as the fingerprint of the document.
        """

        fingerprint = [min(hashes[0:self.w])]
        _prev_index = 0

        for i in range(1, len(hashes)-self.w+1):
            window = hashes[i:i+self.w]
            min_hash = min(window)

            if not (min_hash == fingerprint[-1] and (i <= _prev_index < i+self.w)):
                # the only case where we don't add a new hash to the fingerprint is if the minimum
                # is the same and the previous *specific* hash is still in the window
                _prev_index = len(hashes) - 1 - hashes[::-1].index(min_hash)
                fingerprint.append(min_hash)

        return fingerprint

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


