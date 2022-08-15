from collections import defaultdict

def count_words(words: list):
    words = list(map(str.lower, words))

    word_count = defaultdict(int)

    for w in words:
        # print(w)
        word_count[w] += 1

    return word_count
