def longest_word(sentence):
    if not sentence:
        return None
    words = sentence.lower().split()
    longest_word = ""
    for word in words:
        if len(word) > len(longest_word):
            longest_word = word
    return longest_word

def main():
    print(longest_word("Hello world"))
    print(longest_word("This is a test"))
    print(longest_word("Python is awesome"))
    print(longest_word(""))

if __name__ == "__main__":
    main()