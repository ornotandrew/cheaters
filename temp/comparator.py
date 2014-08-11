def compare():
    a = open("a.py", "r")
    b = open("b.py", "r")
    source_a = a.read()
    source_b = b.read()
    a.close()
    b.close()
    ngrams_a = get_ngrams(source_a)
    ngrams_b = get_ngrams(source_b)
    hashes_a = get_hash_values(ngrams_a)
    hashes_b = get_hash_values(ngrams_b)

    hash_intersection = len(set([x[0] for x in hashes_a]) & set([x[0] for x in hashes_b]))
    fingerprint_a = winnow(hashes_a)
    fingerprint_b = winnow(hashes_b)

    # the percentages below are comparing hashes (numbers) to the number of characters in the files
    # this is not an accurate representation of the size in memory, but is good enough
    print("---Before winnowing---")
    print("File A has {0} hashes, {1} characters, {2:.2f}% of file".format(len(hashes_a), len(source_a),
                                                                           len(hashes_a)/len(source_a)*100))
    print("File B has {0} hashes, {1} characters, {2:.2f}% of file".format(len(hashes_b), len(source_b),
                                                                           len(hashes_b)/len(source_b)*100))
    print("{0} of these are intersect ({1:.2f}%)".format(hash_intersection,
                                                         hash_intersection/min(len(hashes_a), len(hashes_b))*100))
    print("---After winnowing---")
    print("File A has {0} hashes, {1:.2f}% of file".format(len(fingerprint_a),
                                                           len(fingerprint_a)/len(source_a)*100))
    print("File B has {0} hashes, {1:.2f}% of file".format(len(fingerprint_b),
                                                           len(fingerprint_b)/len(source_b)*100))
    print("{0} of these are intersect".format(len(set(x[0] for x in fingerprint_a) & set(x[0] for x in fingerprint_b))))


def get_ngrams(file_contents, n=10):
    """
    :param file_contents: One long, continuous (normalized) string
    :param n: The minimum number of consecutive characters to be a match
    :return A list of the form [ngram, [lines the ngram appears on]]
    """
    ngrams = []

    # generate a map which will tell you what line you are on, given your index in file contents
    index_line_map = [1] + [0]*(len(file_contents)-1)
    for i in range(1, len(file_contents)):
        if file_contents[i-1] == "\n":
            index_line_map[i] = index_line_map[i-1]+1
        else:
            index_line_map[i] = index_line_map[i-1]

    for i in range(len(file_contents)-n+1):
        line_range = list(set(index_line_map[i:i+n]))
        ngrams.append([file_contents[i:i+n], line_range])
    return ngrams


def get_hash_values(ngram_pairs):
    hash_values = [None]*len(ngram_pairs)
    for hash_index in range(len(ngram_pairs)):
        _hash_value = 0
        _current_ngram = ngram_pairs[hash_index][0]
        for i in range(len(_current_ngram)):
            # TODO: use a rolling hash
            _hash_value += ord(_current_ngram[i])*10**(len(_current_ngram)-i-1)
        hash_values[hash_index] = [_hash_value, ngram_pairs[hash_index][1]]
    return hash_values


def winnow(hashes, w=25):
    """
    TODO: Reference this?
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
