def word_count(sentence):
    if not sentence:
        return {}
    words = sentence.lower().split()
    counts = {}
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts