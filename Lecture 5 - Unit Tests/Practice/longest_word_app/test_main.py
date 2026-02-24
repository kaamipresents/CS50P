from main import longest_word

def test_caseDefault():
    assert longest_word("Hello world") == "hello"
    assert longest_word("This is a test") == "this"
    assert longest_word("Python is awesome") == "awesome"
    print("All tests passed!")

def test_caseEmpty():
    assert longest_word("") == None
    print("All tests passed!")