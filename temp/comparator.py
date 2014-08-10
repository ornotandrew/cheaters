def compare():
    a = open("a.py", "r")
    b = open("b.py", "r")
    source_a = a.read()
    print(len(source_a))
    source_b = b.read()
    hashes_a = [get_hash_value(x) for x in get_ngrams(source_a)]
    print(len(hashes_a)*10)
    hashes_b = [get_hash_value(x) for x in get_ngrams(source_b)]
    a.close()
    b.close()
    hash_intersection = len(set(hashes_a) & set(hashes_b))
    fingerprint_a = winnow(hashes_a)
    fingerprint_b = winnow(hashes_b)

    # the percentages below are comparing hashes (numbers) to the number of characters in the files
    # this is not an accurate representation of the size in memory, but is good enough
    print("---Before winnowing---")
    print("File A has {0} hashes, {1:.2f}% of file".format(len(hashes_a),
                                                           len(hashes_a)/len(source_a)*100))
    print("File B has {0} hashes, {1:.2f}% of file".format(len(hashes_b),
                                                           len(hashes_a)/len(source_a)*100))
    print("{0} of these are intersect ({1:.2f}%)".format(hash_intersection,
                                                         hash_intersection/min(len(hashes_a), len(hashes_b))*100))
    print("---After winnowing---")
    print("File A has {0} hashes, {1:.2f}% of file".format(len(fingerprint_a),
                                                           len(fingerprint_a)/len(source_a)*100))
    print("File B has {0} hashes, {1:.2f}% of file".format(len(fingerprint_b),
                                                           len(fingerprint_b)/len(source_b)*100))
    print("{0} of these are intersect".format(len(set(fingerprint_a) & set(fingerprint_b))))


def get_ngrams(file_contents, n=10):
    """
    :param file_contents: One long, continuous (normalized) string
    :param n: The minimum number of consecutive characters to be a match
    """
    ngrams = []
    for i in range(len(file_contents)-n+1):
        ngrams.append(file_contents[i:i+n])
    return ngrams


def get_hash_value(raw_string):
    hash_value = 0
    for i in range(len(raw_string)):
        # TODO: use a rolling hash
        hash_value += ord(raw_string[i])*10**(len(raw_string)-i-1)
    return hash_value


def winnow(hashes, w=25):
    """
    TODO: Reference this?
    We define variables in such a way that:
        1. If there is a substring match at least as long as the guaranteed threshold, t, then this match is detected
        2. We do not detect any matches shorter than the noise threshold, n (used for our ngrams)
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
