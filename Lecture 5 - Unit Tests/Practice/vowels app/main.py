# Count Vowels

def count_vowels(sentence):
    words = sentence.lower().strip().split()
    if not words:
        return 0
    vowels = "aeiou"
    count = 0
    for word in words:
        characters = list(word)
        # print(characters)
        for character in characters:
            if character in vowels:
                count += 1
    return count

def main():
    print(count_vowels("Hello World"))

if __name__ == "__main__":
    main()