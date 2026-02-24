# Reverse Words

def reverse_words(sentence):
    if not sentence:
        return ""
    sentence = sentence.lower().strip().split()
    print(sentence)
    newSentence = []
    for word in sentence:
        NewWord = list(word)
        NewWord.reverse()
        word = "".join(NewWord)
        newSentence.append(word)
    reverse = " ".join(newSentence)
    return reverse

def main():
    print(reverse_words("Kamran Mushtaq is here"))

if __name__ == "__main__":
    main()