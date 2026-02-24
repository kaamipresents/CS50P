# Palindrome app

def is_palindrome(sentence):
    # print(sentence)
    words = sentence.lower().strip().split()
    # print(words)
    # ["Kamran","Madam","Arora"]
    if not words:
        return False
    pallindrime_list = []
    for word in words:
        if word != word[::-1]:
            pass
        else:
            pallindrime_list.append(word)
    return pallindrime_list

def main():
    print(is_palindrome("Kamran Madam Arora"))

if __name__ == "__main__":
    main()


    