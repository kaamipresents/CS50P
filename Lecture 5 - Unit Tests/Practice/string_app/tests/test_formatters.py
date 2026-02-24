from formatters import capitalize_words

def test_case1():
    assert capitalize_words("hello world") == "Hello World"

def test_case2():
    assert capitalize_words("this is a test") == "This Is A Test"

def test_case3():
    assert capitalize_words("python is awesome") == "Python Is Awesome"

print("All tests passed!")