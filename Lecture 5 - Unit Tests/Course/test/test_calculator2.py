# this is done with the pytest feature

from calculator import square

def test_square():
    assert square(2) == 4
    assert square(0) == 0
    assert square(-3) == 9
    print("All tests passed!")

def main():
    test_square()

if __name__ == "__main__":
    main()