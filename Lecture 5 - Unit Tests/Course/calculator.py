def square(n):
    """Returns the square of a number."""
    return n * n


def main():
    # Get input from the user
    num = int(input("Enter a number: "))
    
    # Calculate the square using the separate function
    result = square(num)
    
    # Display the result
    print(f"The square of {num} is {result}")


if __name__ == "__main__":
    main()