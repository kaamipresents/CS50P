from main import word_count


def test_normal_case():
    result = word_count("Hello world hello")
    assert result == {"hello": 2, "world": 1}


def test_case_insensitive():
    result = word_count("Python python PYTHON")
    assert result == {"python": 3}


def test_extra_spaces():
    result = word_count("apple   banana  apple")
    assert result == {"apple": 2, "banana": 1}


def test_empty_string():
    result = word_count("")
    assert result == {}


def test_single_word():
    result = word_count("chatgpt")
    assert result == {"chatgpt": 1}