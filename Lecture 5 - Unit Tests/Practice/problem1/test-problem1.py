from problem1 import calculate_factorial

def test_calculate_factorial():
    assert calculate_factorial(-2) == 1
    assert calculate_factorial(0) == 1
    assert calculate_factorial(1) == 1
    assert calculate_factorial(2) == 2
    assert calculate_factorial(3) == 6
    print("All tests passed!")

def main():
    test_calculate_factorial()

if __name__ == "__main__":
    main()