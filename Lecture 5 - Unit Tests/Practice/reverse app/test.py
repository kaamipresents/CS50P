from main import reverse_words

def test_reverse():
    assert reverse_words("Kamran Mushtaq is here")
    assert reverse_words("This is a test")
    assert reverse_words("Python is awesome")
    print("All tests passed!")

def main():
    test_reverse()

if __name__ == "__main__":
    main()
    