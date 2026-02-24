# this is done with the pytest feature

from calculator import square

def test_positive():
    assert square(1) == 1
    assert square(2) == 4
    assert square(3) == 9
    assert square(4) == 16
    assert square(5) == 25

def test_negative():
    assert square(-1) == 1
    assert square(-2) == 4
    assert square(-3) == 9
    assert square(-4) == 16
    assert square(-5) == 25

def test_zero():
    assert square(0) == 0

def main():
    test_positive()
    test_negative()
    test_zero()
    print("All tests passed!")

if __name__ == "__main__":
    main()