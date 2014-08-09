def compare():
    a = open("temp/a.py", "r")
    b = open("temp/b.py", "r")
    hashes_a = [get_hash_value(x) for x in get_ngrams(a.read())]
    hashes_b = [get_hash_value(x) for x in get_ngrams(b.read())]
    a.close()
    b.close()
    print("File A has", len(hashes_a), "hashes")
    print("File B has", len(hashes_b), "hashes")
    print(len(set(hashes_a) & set(hashes_b)), "of these are intersect")


def get_ngrams(file_contents, n=10):
    ngrams = []
    for i in range(len(file_contents)-n-1):
        ngrams.append(file_contents[i:i+n])
    return ngrams


def get_hash_value(raw_string):
    hash_value = 0
    for i in range(len(raw_string)):
        hash_value += ord(raw_string[i])*10**(len(raw_string)-i-1)
    return hash_value

compare()