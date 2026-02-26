from main import remove_short_words

def test_default():
    assert remove_short_words("Kamran Mushtaq",5) == "kamran mushtaq"
    assert remove_short_words("Kamran Mushtaq",10) == ""
    assert remove_short_words("John Fernandez",5) == "fernandez"
    print("All Tests Passed")

def main():
    test_default()

if __name__ == "__main__":
    main()