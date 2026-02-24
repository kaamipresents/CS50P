from calculator import is_even, square

def test_even():
    assert is_even(2) == True
    assert is_even(3) == False
    print("All tests passed!")

def test_square():
    assert square(2) == 4
    assert square(0) == 0