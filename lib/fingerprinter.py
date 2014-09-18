from collections import deque
from lib.preprocessor import Preprocessor


class Fingerprinter:
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

    def __init__(self, source, filename):
        """
        The process here is as follows:
            normalize -> generate ngrams -> hash ngrams -> winnow
        """
        n = 5
        t = 8
        w = t - n + 1

        pre = Preprocessor(source, filename)
        ngrams = self.get_ngram_lines(pre.processed_source, pre.line_map, n)
        hashes = self.get_hash_values(ngrams)
        self.fingerprint = self.winnow(hashes, w)

    @staticmethod
    def get_ngram_lines(source, line_map, n):
        """
        :param source: One long, continuous (normalized) string
        :param n: The minimum number of consecutive characters to be a match
        :return A list of the containing elements of the form [ngram, [lines the ngram appears on]]
        """

        ngrams = []
        for i in range(len(source)-n+1):
            line_range_raw = line_map[i:i+n]
            line_range = list(set([x for x in line_range_raw if line_range_raw.count(x) > 1]))
            ngrams.append([source[i:i+n], line_range])

        # there may be a case where the whole file has less than n characters
        if len(ngrams) == 0:
            return [[source, [1]]]

        return ngrams

    @staticmethod
    def get_hash_values(ngram_list):
        """
        This replaces the ngrams with their hashes instead of making a new list
        :return: the original ngram_pairs, but now of the form [hash, [lines the ngram appears on]]
        """

        base_seed = 10

        # run the first hash normally
        first_hash_in_prev_window = 0
        current_ngram = ngram_list[0][0]
        hash_value = 0
        for i in range(len(current_ngram)):
            hash_value += ord(current_ngram[i])*base_seed**(len(current_ngram)-i-1)
            if i == 0:
                first_hash_in_prev_window = hash_value
        ngram_list[0] = [hash_value, ngram_list[0][1]]

        # then use the rolling function
        for hash_index in range(1, len(ngram_list)):
            current_ngram = ngram_list[hash_index][0]
            temp = ord(current_ngram[0])*base_seed**(len(current_ngram)-1)
            prev_hash = ngram_list[hash_index-1][0]
            ngram_list[hash_index][0] = (prev_hash - first_hash_in_prev_window)*base_seed + ord(ngram_list[hash_index][0][-1])
            first_hash_in_prev_window = temp

        return ngram_list

    @staticmethod
    def winnow(hashes, w):
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

        fingerprint = [min(hashes[0:w])]
        prev_index = 0

        for i in range(1, len(hashes)-w+1):
            window = hashes[i:i+w]
            min_hash = min(window)

            if not (min_hash == fingerprint[-1] and (i <= prev_index < i+w)):
                # the only case where we don't add a new hash to the fingerprint is if the minimum
                # is the same and the previous *specific* hash is still in the window
                prev_index = len(hashes) - 1 - hashes[::-1].index(min_hash)
                fingerprint.append(min_hash)

        return fingerprint

    @staticmethod
    def ngram_generator(x, n):
        """
        A fast way of generating ngrams
        :param x: Any iterable (string, list)
        :param n: The number of elements in each gram
        :return: The next ngram
        """
        gram = deque(x[:n], n)
        yield list(gram)
        for char in x[n+1:]:
            gram.append(char)
            yield list(gram)






