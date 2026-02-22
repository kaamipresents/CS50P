from calculator import square

def test_square():
    if square(2) != 4:
        print("Test failed: square(2) != 4")
    if square(0) != 0:
        print("Test failed: square(0) != 0")
    if square(-3) != 9:
        print("Test failed: square(-3) != 9")
    print("All tests passed!")

def main():
    test_square()

if __name__ == "__main__":
    main()