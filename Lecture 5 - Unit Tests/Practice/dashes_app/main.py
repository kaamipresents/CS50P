# Add Dashes Between Words

def dashify(sentence):
    if not sentence:
        return ""
    words = sentence.lower().strip().split()
    newSentence = "-".join(words)
    print(newSentence)
    return newSentence

def main():
    dashify("Kamran Mushtaq")
    dashify("     Game    Offline")

if __name__ == "__main__":
    main()
