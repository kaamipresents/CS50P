from main import count_vowels

def test_vowels():
    assert count_vowels("Hello World") == 3
    assert count_vowels("This is a test") == 4
    assert count_vowels("Python is awesome") == 6
    print("All tests passed!")

def main():
    test_vowels()

if __name__ == "__main__":
    main()