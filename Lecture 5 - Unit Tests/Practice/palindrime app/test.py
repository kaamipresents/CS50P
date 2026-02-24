from main import is_palindrome

def test_palindrime():
    assert is_palindrome("Kamran Madam Arora") == ["madam","arora"]
    assert is_palindrome("This is a test") == ['a']
    assert is_palindrome("Python is awesome") == []
    print("All tests passed!")

def main():
    test_palindrime()

if __name__ == "__main__":
    main()