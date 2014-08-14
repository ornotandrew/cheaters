import time
class Comparator:
    def __init__(self, source_a, source_b):
        self.source_a = source_a
        self.source_b = source_b
        self.n = 10
        self.w = 6

    def compare(self):

        ngrams_a = self.get_ngrams(self.source_a)
        ngrams_b = self.get_ngrams(self.source_b)
        hashes_a = self.get_hash_values(ngrams_a)
        hashes_b = self.get_hash_values(ngrams_b)
        fingerprint_a = self.winnow(hashes_a)
        fingerprint_b = self.winnow(hashes_b)

        # the percentages below are comparing hashes (numbers) to the number of characters in the files
        # this is not an accurate representation of the size in memory, but is good enough
        result = self.compare_fingerprints(fingerprint_a, fingerprint_b)

        # make result[0] a percentage of total lines, since we have the sources up here
        # we don't want to count blank lines, because we are not matching on blank lines
        num_lines_a = len([x for x in self.source_a.split("\n") if x != ""])
        num_lines_b = len([x for x in self.source_b.split("\n") if x != ""])

        result[0] = int(result[0]/min(num_lines_a, num_lines_b)*100)

        return result


    def get_ngrams(self, file_contents):
        """
        :param file_contents: One long, continuous (normalized) string
        :param n: The minimum number of consecutive characters to be a match
        :return A list of the containing elements of the form [ngram, [lines the ngram appears on]]
        """
        ngrams = []
        n = self.n
        # generate a map which will tell you what line you are on, given your index in file contents
        index_line_map = [1] + [0]*(len(file_contents)-1)
        for i in range(1, len(file_contents)):
            if file_contents[i-1] == "\n":
                index_line_map[i] = index_line_map[i-1]+1
            else:
                index_line_map[i] = index_line_map[i-1]

        for i in range(len(file_contents)-n+1):
            line_range_raw = index_line_map[i:i+n]
            line_range = list(set([x for x in line_range_raw if line_range_raw.count(x) > 1]))
            ngrams.append([file_contents[i:i+n], line_range])

        return ngrams


    def get_hash_values(self, ngram_list):
        """
        This replaces the ngrams with their hashes instead of making a new list
        :return: the original ngram_pairs, but now of the form [hash, [lines the ngram appears on]]
        """

        # run the first hash normally
        _first_hash_in_prev_window = 0
        _current_ngram = ngram_list[0][0]
        _hash_value = 0
        for i in range(len(_current_ngram)):
            _hash_value += ord(_current_ngram[i])*10**(len(_current_ngram)-i-1)
            if i == 0:
                _first_hash_in_prev_window = _hash_value
        ngram_list[0][0] = _hash_value

        # then use the rolling function
        for hash_index in range(1, len(ngram_list)):
            _current_ngram = ngram_list[hash_index][0]
            _temp = ord(_current_ngram[0])*10**(len(_current_ngram)-1)
            _prev_hash = ngram_list[hash_index-1][0]
            ngram_list[hash_index][0] = (_prev_hash - _first_hash_in_prev_window)*10 + ord(ngram_list[hash_index][0][-1])
            _first_hash_in_prev_window = _temp

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
        w = self.w
        fingerprint = [min(hashes[0:w])]
        _prev_index = 0

        for i in range(1, len(hashes)-w+1):
            window = hashes[i:i+w]
            min_hash = min(window)

            if not (min_hash == fingerprint[-1] and (i <= _prev_index < i+w)):
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

        result[0] = len(hash_map)
        result[1] = sorted(list(hash_map.values()))
        return result


