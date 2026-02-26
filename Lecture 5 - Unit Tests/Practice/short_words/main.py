# Remove Short Words

def remove_short_words(sentence, min_length):
    if not sentence:
        return ""
    words = sentence.lower().strip().split()
    # print(words)
    new_Words = []
    for word in words:
        if len(word) < min_length:
            pass
        else:
            new_Words.append(word)
    newSentence = " ".join(new_Words)
    # print(newSentence)
    return newSentence

def main():
    print(remove_short_words("Kamran Mushtaq",10))
    print(remove_short_words("Rabia Ali",5))

if __name__ == "__main__":
    main()